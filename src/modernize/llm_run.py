"""Deterministic validation/retry flow and redacted, recomputable usage logs."""

from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from decimal import Decimal
import json
import math
import os
from pathlib import Path
import time

from pydantic import ValidationError

from modernize.llm import LLMResponse, MockLLMClient, ProviderError, TokenUsage
from modernize.llm_prompts import Prompt, load_prompt, strict_json
from modernize.openai_client import redact


@dataclass(frozen=True)
class RateCard:
    model: str
    input_per_million: Decimal
    cached_input_per_million: Decimal
    output_per_million: Decimal
    source: str
    checked_on: str

    def __post_init__(self):
        if not isinstance(self.model, str) or not self.model or not isinstance(self.source, str) or not self.source:
            raise ValueError('pricing model and source are required')
        date.fromisoformat(self.checked_on)
        for value in (self.input_per_million, self.cached_input_per_million, self.output_per_million):
            if not isinstance(value, Decimal) or not value.is_finite() or value < 0:
                raise ValueError('rates must be finite nonnegative Decimal values')

    def cost(self, usage):
        if usage.cache_write_tokens:
            raise ValueError('cache-write pricing is not configured; cost is unknown')
        return ((usage.input_tokens - usage.cached_input_tokens) * self.input_per_million +
                usage.cached_input_tokens * self.cached_input_per_million +
                usage.output_tokens * self.output_per_million) / Decimal(1000000)

    def record(self):
        result = asdict(self)
        for key in ('input_per_million', 'cached_input_per_million', 'output_per_million'):
            result[key] = str(result[key])
        return result


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    call_timeout_seconds: float = 15
    retry_window_seconds: float = 60
    backoff_seconds: float = 0.5
    max_backoff_seconds: float = 10

    def __post_init__(self):
        if type(self.max_attempts) is not int or not 1 <= self.max_attempts <= 5:
            raise ValueError('max_attempts must be 1..5')
        for key in ('call_timeout_seconds', 'retry_window_seconds', 'backoff_seconds', 'max_backoff_seconds'):
            value = getattr(self, key)
            if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
                raise ValueError('retry timings must be finite nonnegative numbers')
        if not 0 < self.call_timeout_seconds <= 120 or not 0 < self.retry_window_seconds <= 600:
            raise ValueError('positive call timeout <=120 and retry window <=600 required')
        if self.max_backoff_seconds > 30 or self.backoff_seconds > self.max_backoff_seconds:
            raise ValueError('backoff must fit its cap, at most 30 seconds')


def usage_summary(records):
    totals = dict(input_tokens=0, output_tokens=0, cached_input_tokens=0, cache_write_tokens=0)
    cost = Decimal(0)
    unknown_usage = unknown_cost = 0
    for record in records:
        usage = record['usage']
        if usage is None:
            unknown_usage += 1
            unknown_cost += 1
            continue
        tokens = TokenUsage(**usage)
        for key in totals:
            totals[key] += getattr(tokens, key)
        rates = record['pricing'].copy()
        for key in ('input_per_million', 'cached_input_per_million', 'output_per_million'):
            rates[key] = Decimal(rates[key])
        try:
            cost += RateCard(**rates).cost(tokens)
        except ValueError:
            unknown_cost += 1
    return dict(attempts=len(records), known_tokens=totals,
                known_total_tokens=totals['input_tokens'] + totals['output_tokens'],
                unknown_usage_attempts=unknown_usage, unknown_cost_attempts=unknown_cost,
                known_estimated_usd=str(cost), usage_complete=unknown_usage == 0,
                cost_complete=unknown_cost == 0)


def recompute_usage(directory):
    path = Path(directory) / 'calls.jsonl'
    records = [strict_json(line) for line in path.read_text().splitlines()]
    return usage_summary(records)


class LLMStageFailure(ValueError):
    pass


class LLMRun:
    def __init__(self, client, output, rates, policy=None, *, evidence_kind=None):
        if rates.model != client.model:
            raise ValueError('rate-card model must match the requested client model')
        evidence_kind = evidence_kind or ('mock' if isinstance(client, MockLLMClient) else 'provider')
        if isinstance(client, MockLLMClient) and evidence_kind != 'mock':
            raise ValueError('mock usage cannot be labeled as provider usage')
        if evidence_kind not in ('provider', 'mock', 'sdk_http_fixture'):
            raise ValueError('invalid usage provenance')
        self.client, self.rates, self.policy = client, rates, policy or RetryPolicy()
        self.output = Path(output)
        self.output.mkdir(mode=0o700, parents=True, exist_ok=False)
        self.log = self.output / 'calls.jsonl'
        self.log.touch(mode=0o600, exist_ok=False)
        self.records = []
        self.evidence_kind = evidence_kind
        self.secrets = tuple(getattr(client, 'secrets', ())) + tuple(
            value for key, value in os.environ.items() if key in ('OPENAI_API_KEY', 'OPENAI_ADMIN_KEY') and value)
        self._write_summary('ready')

    def _safe(self, value):
        # Redact after serialization too, so escaped secret strings cannot leak.
        text = json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False)
        secrets = self.secrets + tuple(json.dumps(s, ensure_ascii=True)[1:-1] for s in self.secrets)
        return redact(text, secrets)

    def _write_summary(self, status):
        summary = dict(status=status, evidence_kind=self.evidence_kind, policy=asdict(self.policy),
                       **usage_summary(self.records))
        temporary = self.output / 'summary.tmp'
        temporary.write_text(self._safe(summary) + '\n')
        temporary.replace(self.output / 'summary.json')

    def generate(self, prompt_name, context):
        prompt = prompt_name if isinstance(prompt_name, Prompt) else load_prompt(prompt_name)
        prompt_name = prompt.name
        base = prompt.render(context)
        if len(base.encode()) > 64000:
            raise ValueError('rendered prompt exceeds 64000 bytes')
        deadline = time.monotonic() + self.policy.retry_window_seconds
        feedback = ''
        last_error = 'retry window exhausted'
        for attempt in range(1, self.policy.max_attempts + 1):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            request = redact(base + feedback, self.secrets)
            response = None
            value = None
            validation = 'not_run'
            retryable, retry_after = True, None
            error_code = None
            started = time.monotonic()
            try:
                response = self.client.complete(request, response_schema=prompt.schema,
                                                timeout_seconds=min(self.policy.call_timeout_seconds, remaining))
                if not isinstance(response, LLMResponse) or not isinstance(response.text, str) or \
                        not isinstance(response.model, str) or (response.usage is not None and
                                                               not isinstance(response.usage, TokenUsage)):
                    raise ValueError('invalid client response metadata')
                if len(response.text.encode()) > 128000:
                    raise ValueError('response exceeds 128000 bytes')
                decoded = strict_json(response.text)
                value = prompt.response_model.model_validate(decoded, strict=True)
                validation = 'passed'
                last_error = ''
            except ProviderError as error:
                response = error.response
                last_error = str(error)
                error_code, retryable, retry_after = error.code, error.retryable, error.retry_after
            except ValidationError as error:
                validation = 'failed'
                last_error = json.dumps(error.errors(include_input=False, include_context=False, include_url=False))
                error_code = 'validation'
            except (ValueError, TypeError, RecursionError) as error:
                validation = 'failed'
                last_error, error_code = str(error), 'validation'
            except Exception as error:
                last_error, error_code, retryable = str(error), 'client_error', False
            if time.monotonic() > deadline:
                value, retryable = None, False
                last_error, error_code = 'retry window exhausted', 'deadline'
            last_error = redact(last_error, self.secrets)[:2000]
            delay = min(self.policy.backoff_seconds * (2 ** (attempt - 1)), self.policy.max_backoff_seconds)
            if retry_after is not None:
                delay = retry_after
            will_retry = value is None and retryable and attempt < self.policy.max_attempts and \
                0 <= delay <= self.policy.max_backoff_seconds and time.monotonic() + delay < deadline
            record = dict(timestamp=datetime.now(timezone.utc).isoformat(), prompt_version=prompt_name,
                          attempt=attempt, requested_model=self.client.model,
                          model=response.model if isinstance(response, LLMResponse) else self.client.model,
                          prompt=request, response=response.text if isinstance(response, LLMResponse) else None,
                          response_id=response.response_id if isinstance(response, LLMResponse) else None,
                          usage=asdict(response.usage) if isinstance(response, LLMResponse) and response.usage else None,
                          pricing=self.rates.record(), evidence_kind=self.evidence_kind,
                          validation=dict(status=validation, error=last_error or None), error_code=error_code,
                          elapsed_seconds=time.monotonic() - started, will_retry=will_retry,
                          retry_after_seconds=retry_after, retry_delay_seconds=delay if will_retry else None)
            sanitized = strict_json(self._safe(record))
            with self.log.open('a') as stream:
                stream.write(json.dumps(sanitized, sort_keys=True) + '\n')
            self.records.append(sanitized)
            self._write_summary('passed' if value is not None else 'retrying' if will_retry else 'failed')
            if value is not None:
                return value
            if not will_retry:
                break
            if validation == 'failed':
                feedback = '\nPrevious response failed validation. Return corrected JSON. Error: ' + last_error
            if delay:
                time.sleep(delay)
        self._write_summary('failed')
        raise LLMStageFailure(redact(f'{prompt_name} failed: {last_error}; records: {self.output}', self.secrets)) from None
