# CP4 LLM layer

`LLMRun` controls validation, retry routing and accounting. `OpenAIClient` uses
the official OpenAI Responses SDK directly; `MockLLMClient` supplies deterministic
or scripted replies. The LLM cannot choose stages, execute tools or write files.
No agent framework is installed. The existing CLI configuration remains unchanged;
CP4 is a Python API used by later stages.

## Setup and credentials

Install the project in its virtual environment (`pip install -e .`). Runtime
dependencies are pinned to OpenAI SDK 3.55.1 and Pydantic 2.14.3, the versions
verified here. SDK 3.55.1 uses HTTPX2; offline integration tests use its
`MockTransport`, exercising real SDK serialization, HTTP error mapping and
response objects with no outgoing provider requests.

For paid calls, set `OPENAI_API_KEY` outside the repository and construct
`OpenAIClient(model=...)` with an explicitly chosen supported model. No model or
tariff is silently selected. Supply a `RateCard` with matching model, finite
nonnegative Decimal input/cached-input/output USD-per-million rates, their source
and the date checked. Obtain rates from the provider's official pricing for
that model. The client must remain on the trusted controller; never forward its
key, client or network access into legacy/modern execution containers.

The public stage-facing operation is `LLMRun.generate(prompt_version, context)`.
Low-level `complete` returns raw provider data for the validation layer; later
stages must not consume it directly. An offline example:

```python
import json
from datetime import date
from decimal import Decimal
from modernize.llm import MockLLMClient
from modernize.llm_run import LLMRun, RateCard

reply = {"cases": [{"category": "typical", "args_json": "[1,2]",
                    "kwargs_json": "{}", "reason": "Two integer inputs."}]}
client = MockLLMClient(response=json.dumps(reply))
rates = RateCard(client.model, Decimal(0), Decimal(0), Decimal(0),
                 "mock; no provider billing", date.today().isoformat())
run = LLMRun(client, "artifacts/new-llm-run", rates)
proposals = run.generate("input_proposals.v1", {"function": "example(a,b)"})
```

The output directory must be new. Logs live under a private directory with
owner-only `calls.jsonl`. Nothing in this example executes the proposed inputs,
creates characterization fixtures or predicts results; those are CP5 work.

## Prompt and validation contract

The first registered prompt is `input_proposals.v1`. Its `.txt` template and
`.schema.json` are separate versioned package data. `load_prompt` checks the stored
schema exactly matches its registered strict Pydantic model. Unit tests enumerate
all templates and require schema/mock coverage; the wheel packaging check also
loads the prompt/schema from the built distribution.

The only response field is `cases`: 1–32 input proposals. Each has `category`
(`typical`, `edge`, `empty`, `boundary`, `unicode`, `bytes`), `args_json`,
`kwargs_json`, and a short `reason`. Extra fields, including expected outputs
and assertions, are forbidden. Argument strings must parse as a positional array
and keyword object. Nested binary inputs use exactly `{"$bytes":"BASE64"}`;
the encoding is validated here, but runtime decoding/execution belongs to CP5.
Duplicate JSON keys, nonfinite numbers, invalid bytes and nesting beyond 30
levels are rejected. Arguments are data, never code.

Rendering JSON-encodes context, marks it as untrusted data and includes the
schema. The provider requests strict JSON-schema output, but local validation is
still mandatory. Refusals and incomplete provider responses cannot be accepted
as valid stage data. No template emits source code in CP4, so compilation and
execution validation apply when code-producing stages are introduced.

## Retry and timeout policy

- Default: at most three attempts (configurable 1–5), 15-second SDK I/O timeouts,
  60-second retry window, exponential backoff from 0.5 seconds capped at 10.
- SDK automatic retries are disabled per attempt, even for an injected client
  configured otherwise. Logged attempt counts therefore match HTTP attempts.
- JSON/schema/argument validation failures feed a bounded, sanitized error into
  the next prompt. Invalid outputs never escape `generate`.
- Connection errors, timeouts, HTTP 408/409/429 and 5xx responses may retry;
  authentication errors and refusals fail immediately. Retry-After seconds,
  HTTP dates and milliseconds are recognized. A required delay beyond the cap
  or remaining window stops cleanly instead of retrying early.
- A late response cannot pass the retry window. SDK timeouts apply to I/O phases,
  not a killable process deadline; the retry window bounds decisions, not arbitrary
  blocking code inside a third-party transport. Custom clients must honor the
  timeout contract. Real slow-network timing has not been tested here.

Rendered prompts are capped at 64,000 bytes, responses accepted for validation
at 128,000 bytes and provider output tokens at a configured bound (default 2048,
maximum 8192). These are attempt/token bounds, not a hard prepaid USD budget.
The model never receives tools and provider response storage is disabled.

## Records, secrets and cost accounting

Every attempt appends timestamp, prompt version, requested/returned model,
sanitized prompt/response, response ID, token usage, dated tariff, validation
result/error, timing, error category and retry decision to `calls.jsonl`.
`summary.json` updates after each attempt and on final failure; a capped failure
raises `LLMStageFailure` with a sanitized message and record path.

Known credential values, credential patterns and Bearer tokens are removed
before sending prompts and before writing logs/errors. Serialization is also
sanitized to cover escaped values. Tests generate fake credentials in memory,
exercise response/error echoes and inspect SDK DEBUG logs; no credential is
committed. Do not treat redaction as a general scrubber for all private project
data or arbitrary unknown secret encodings.

Usage and estimates include failed validation, refusals, incomplete replies and
every retry. Pricing is Decimal arithmetic:

`((input - cached) * input_rate + cached * cached_rate + output * output_rate) / 1_000_000`

API totals must match input plus output; counts must be nonnegative integers and
cached/cache-write input cannot exceed total input. Reasoning tokens are already
inside reported output totals, not added twice. Nonzero cache-write usage without
a configured separate tariff is flagged as unknown cost. No tools/image charges
are estimated because this integration requests text with no tools.

`known_tokens`, `known_total_tokens`, `known_estimated_usd`, unknown usage/cost
attempt counts and completeness flags distinguish partial accounting from zero
usage. A timed-out request may have consumed tokens; missing usage is never
invented as zero. Estimates use the supplied tariff and are not provider invoices.
Mock and intercepted-HTTP runs are explicitly labeled; mock usage cannot be
misrepresented as provider usage. `recompute_usage(directory)` rebuilds totals
from attempt logs; no report counters are hand-entered.

## Recorded verification

Use `.venv/bin/python scripts/test.py` (or activate the environment first).
CP4 tests run offline; CP3's live Docker tests retain their explicit opt-in.
[CP4 evidence](evidence/cp4.json) contains eight SDK/HTTP fixture scenarios,
their fourteen intercepted attempts, and a three-attempt deterministic mock
failure. Fixture token counts and tariffs are simulated, not model measurements
or money spent. No live authenticated provider call or model-quality benchmark
is claimed. Existing characterization/held-out/coverage work remains unstarted.

Official references used for the implementation:

- [OpenAI Python SDK: API, retries and timeouts](https://github.com/openai/openai-python)
- [OpenAI structured outputs and refusal/incomplete handling](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Pydantic strict validation](https://docs.pydantic.dev/latest/concepts/strict_mode/)
