"""Direct OpenAI Responses SDK adapter; orchestration/retries live in LLMRun."""

import math
import os
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI

from modernize.llm import LLMResponse, ProviderError, TokenUsage


def redact(text, secrets=()):
    for secret in secrets:
        if secret:
            text = text.replace(secret, '[REDACTED]')
    text = re.sub(r'\bsk-[A-Za-z0-9_-]{8,}', '[REDACTED]', text)
    return re.sub(r'(?i)\bbearer\s+[^\s"\\]+', 'Bearer [REDACTED]', text)


class OpenAIClient:
    def __init__(self, model, *, sdk=None, max_output_tokens=2048):
        if not isinstance(model, str) or not model or any(c.isspace() for c in model):
            raise ValueError('model must be an explicit nonempty model identifier')
        if type(max_output_tokens) is not int or not 1 <= max_output_tokens <= 8192:
            raise ValueError('max_output_tokens must be 1..8192')
        self.model = model
        self.max_output_tokens = max_output_tokens
        self.sdk = sdk if sdk is not None else OpenAI(max_retries=0)
        self.secrets = tuple(s for s in (getattr(self.sdk, 'api_key', None),
                                        os.environ.get('OPENAI_API_KEY')) if isinstance(s, str) and s)

    def complete(self, prompt, *, response_schema=None, timeout_seconds=15):
        if not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
            raise ValueError('timeout must be finite and positive')
        format = (dict(type='json_schema', name='stage_response', strict=True, schema=response_schema)
                  if response_schema is not None else dict(type='json_object'))
        try:
            response = self.sdk.with_options(max_retries=0, timeout=timeout_seconds).responses.create(
                model=self.model, instructions='Return JSON for the requested stage. Never use tools or choose pipeline stages.',
                input=prompt, text={'format': format}, max_output_tokens=self.max_output_tokens,
                store=False, tools=[])
        except (APITimeoutError, APIConnectionError) as error:
            code = 'timeout' if isinstance(error, APITimeoutError) else 'connection'
            raise ProviderError(redact(str(error), self.secrets), code=code, retryable=True) from None
        except APIStatusError as error:
            headers = error.response.headers
            header = headers.get('retry-after-ms') or headers.get('retry-after')
            try:
                if headers.get('retry-after-ms') is not None:
                    retry_after = float(header) / 1000
                else:
                    try:
                        retry_after = float(header) if header is not None else None
                    except ValueError:
                        retry_after = max(0, (parsedate_to_datetime(header) - datetime.now(timezone.utc)).total_seconds())
                if retry_after is not None and (not math.isfinite(retry_after) or retry_after < 0):
                    retry_after = None
            except (ValueError, TypeError, OverflowError):
                retry_after = None
            raise ProviderError(redact(str(error), self.secrets), code=f'http_{error.status_code}',
                                retryable=error.status_code in (408, 409, 429) or error.status_code >= 500,
                                retry_after=retry_after) from None
        usage = None
        if response.usage is not None:
            raw = response.usage
            try:
                usage = TokenUsage(raw.input_tokens, raw.output_tokens,
                                   raw.input_tokens_details.cached_tokens,
                                   raw.input_tokens_details.cache_write_tokens)
                if raw.total_tokens != usage.input_tokens + usage.output_tokens:
                    raise ValueError('provider total token count is inconsistent')
            except (ValueError, AttributeError):
                raise ProviderError('invalid provider token usage', code='usage_invalid') from None
        result = LLMResponse(response.output_text, response.model, usage, response.id)
        if any(getattr(part, 'type', None) == 'refusal' for item in response.output
               for part in (getattr(item, 'content', None) or [])):
            raise ProviderError('provider refused the response', code='refusal', response=result)
        if response.status != 'completed':
            raise ProviderError('provider response did not complete', code='incomplete',
                                retryable=True, response=result)
        return result
