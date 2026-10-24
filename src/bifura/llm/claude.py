"""Anthropic Claude adapter (official `anthropic` SDK). Install: pip install anthropic"""

from __future__ import annotations

from typing import Any

from bifura.llm.base import LLMError
from bifura.llm.gemini import _parse_json

DEFAULT_MODEL = "claude-opus-5-5"


class ClaudeClient:
    provider = "claude"

    def __init__(self, api_key: str, model: str | None = None):
        try:
            import anthropic
        except ImportError as exc:
            raise LLMError("The Claude adapter needs the SDK: pip install anthropic") from exc
        self._anthropic = anthropic
        self._client = anthropic.Anthropic(api_key=api_key, timeout=120.0, max_retries=2)
        self.model = model or DEFAULT_MODEL

    def next_json(self, system: str, turns: list[dict[str, str]]) -> dict[str, Any]:
        a = self._anthropic
        messages = [{"role": "assistant" if t["role"] == "model" else "user", "content": t["text"]} for t in turns]
        try:
            # Server-side refusal fallback ("default" routing) is on, so a safety decline is retried
            # on another model inside the same call instead of failing the investigation.
            resp = self._client.beta.messages.create(
                model=self.model, max_tokens=16000, system=system + "\nReply with one JSON object only.",
                messages=messages, betas=["server-side-fallback-2026-07-01"], fallbacks="default")
        except a.AuthenticationError as exc:
            raise LLMError(f"Claude rejected the API key: {exc}") from exc
        except a.NotFoundError as exc:
            raise LLMError(f"Claude model not found ({self.model}); set CLAUDE_MODEL: {exc}") from exc
        except a.RateLimitError as exc:
            raise LLMError(f"Claude is rate-limited: {exc}") from exc
        except a.APIStatusError as exc:
            raise LLMError(f"Claude API error {exc.status_code}: {exc.message}") from exc
        except a.APIConnectionError as exc:
            raise LLMError(f"Could not reach Claude: {exc}") from exc
        if resp.stop_reason == "refusal":
            raise LLMError("Claude declined this request.")
        text = "".join(b.text for b in resp.content if b.type == "text")
        return _parse_json(text)
