"""Provider-neutral call boundary and deterministic scripted mock."""

from dataclasses import dataclass, field
import math
from typing import Protocol


@dataclass(frozen=True)
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    cached_input_tokens: int = 0
    cache_write_tokens: int = 0

    def __post_init__(self):
        if any(type(v) is not int or v < 0 for v in vars(self).values()):
            raise ValueError('token counts must be nonnegative integers')
        if self.cached_input_tokens + self.cache_write_tokens > self.input_tokens:
            raise ValueError('cached/write tokens cannot exceed input tokens')


@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str
    usage: TokenUsage | None = None
    response_id: str | None = None

    def __post_init__(self):
        if not isinstance(self.text, str) or not isinstance(self.model, str) or not self.model:
            raise ValueError('response text/model must be strings with a nonempty model')
        if self.usage is not None and not isinstance(self.usage, TokenUsage):
            raise ValueError('response usage must be TokenUsage or unknown')
        if self.response_id is not None and not isinstance(self.response_id, str):
            raise ValueError('response ID must be a string or absent')


class ProviderError(Exception):
    def __init__(self, message, *, code, retryable=False, retry_after=None, response=None):
        if not isinstance(code, str) or type(retryable) is not bool:
            raise ValueError('provider error requires a code and boolean retry flag')
        if retry_after is not None and (type(retry_after) not in (int, float) or
                                       not math.isfinite(retry_after) or retry_after < 0):
            raise ValueError('retry-after must be finite and nonnegative')
        if response is not None and not isinstance(response, LLMResponse):
            raise ValueError('provider error response must be LLMResponse or absent')
        super().__init__(message)
        self.code, self.retryable = code, retryable
        self.retry_after, self.response = retry_after, response


class LLMClient(Protocol):
    model: str
    def complete(self, prompt: str, *, response_schema=None, timeout_seconds=15) -> LLMResponse: ...


@dataclass(frozen=True)
class MockLLMClient:
    response: str = '{"inputs": []}'
    model: str = 'deterministic-mock'
    replies: tuple = ()
    calls: list[str] = field(default_factory=list, compare=False, repr=False)

    def complete(self, prompt: str, *, response_schema=None, timeout_seconds=15) -> LLMResponse:
        self.calls.append(prompt)
        if self.replies:
            index = len(self.calls) - 1
            if index >= len(self.replies):
                raise ProviderError('mock reply sequence exhausted', code='mock_exhausted')
            reply = self.replies[index]
            if isinstance(reply, Exception):
                raise reply
            return reply if isinstance(reply, LLMResponse) else LLMResponse(reply, self.model, TokenUsage())
        return LLMResponse(text=self.response, model=self.model, usage=TokenUsage())
