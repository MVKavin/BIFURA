"""OpenAI GPT adapter (official `openai` SDK). Install: pip install openai"""

from __future__ import annotations

from typing import Any

from bifura.llm.base import LLMError
from bifura.llm.gemini import _parse_json

DEFAULT_MODEL = "gpt-5-mini"  # override with OPENAI_MODEL


class OpenAIClient:
    provider = "gpt"

    def __init__(self, api_key: str, model: str | None = None):
        try:
            import openai
        except ImportError as exc:
            raise LLMError("The GPT adapter needs the SDK: pip install openai") from exc
        self._openai = openai
        self._client = openai.OpenAI(api_key=api_key, timeout=120.0, max_retries=2)
        self.model = model or DEFAULT_MODEL

    def next_json(self, system: str, turns: list[dict[str, str]]) -> dict[str, Any]:
        o = self._openai
        messages = [{"role": "system", "content": system + "\nReply with one JSON object only."}]
        import base64
        for t in turns:
            content: Any = t["text"]
            if t.get("image"):
                data, mime = t["image"]
                url = f"data:{mime};base64,{base64.standard_b64encode(data).decode()}"
                content = [{"type": "text", "text": t["text"]}, {"type": "image_url", "image_url": {"url": url}}]
            messages.append({"role": "assistant" if t["role"] == "model" else "user", "content": content})
        try:
            resp = self._client.chat.completions.create(model=self.model, messages=messages,
                                                        response_format={"type": "json_object"})
        except o.AuthenticationError as exc:
            raise LLMError(f"OpenAI rejected the API key: {exc}") from exc
        except o.NotFoundError as exc:
            raise LLMError(f"OpenAI model not found ({self.model}); set OPENAI_MODEL: {exc}") from exc
        except o.RateLimitError as exc:
            raise LLMError(f"OpenAI is rate-limited or out of credit: {exc}") from exc
        except o.APIError as exc:
            raise LLMError(f"OpenAI API error: {exc}") from exc
        return _parse_json(resp.choices[0].message.content or "")
