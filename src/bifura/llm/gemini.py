"""Google Gemini adapter (google-genai SDK)."""

from __future__ import annotations

import json
import os
import re
import time
from typing import Any

from bifura.llm.base import LLMError

# Google retired gemini-2.5-flash for new users and recommends gemini-3.8-flash (Oct 2026).
FALLBACK_MODEL = "gemini-3.8-flash"
FALLBACK_CHAIN = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash", "gemini-flash-latest",
                  "gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-flash-lite-latest", "gemini-2.5-flash-lite"]
ROUNDS = 3          # passes over the whole chain when every model is busy
ROUND_WAIT_S = 8    # pause between passes


def _parse_json(text: str) -> dict[str, Any]:
    text = (text or "").strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.S)
    if fenced:
        text = fenced.group(1)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end <= start:
            raise LLMError(f"Model reply was not JSON: {text[:200]!r}")
        data = json.loads(text[start:end + 1])
    if not isinstance(data, dict):
        raise LLMError("Model reply was JSON but not an object.")
    return data


def pick_model(client: Any) -> str:
    """Choose the newest stable Gemini *flash* text model this key can use."""
    try:
        names = []
        for m in client.models.list():
            name = (m.name or "").removeprefix("models/")
            actions = m.supported_actions or []
            if "generateContent" not in actions or "flash" not in name:
                continue
            if any(x in name for x in ("lite", "image", "tts", "live", "audio", "embedding", "exp", "preview", "thinking")):
                continue
            names.append(name)
        nums = lambda n: [float(x) for x in re.findall(r"\d+(?:\.\d+)?", n)] or [0.0]
        return max(names, key=nums) if names else FALLBACK_MODEL
    except Exception:
        return FALLBACK_MODEL


class GeminiClient:
    provider = "gemini"

    def __init__(self, api_key: str, model: str | None = None, temperature: float = 0.2, timeout_s: int = 90):
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:  # pragma: no cover
            raise LLMError("google-genai is not installed: pip install google-genai") from exc
        self._types = types
        # Gemini Developer API by default (works for both "AIza…" and "AQ." AI Studio keys).
        # Set GOOGLE_GENAI_USE_VERTEXAI=true only for a Vertex AI project with the API enabled.
        self.vertex = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "").lower() in ("1", "true")
        http = types.HttpOptions(timeout=timeout_s * 1000)
        self._client = (genai.Client(vertexai=True, api_key=api_key, http_options=http) if self.vertex
                        else genai.Client(api_key=api_key, http_options=http))
        # Listing models can be slow, so use a known current default unless LLM_MODEL pins one.
        self.model = model or FALLBACK_MODEL
        self.temperature = temperature

    def next_json(self, system: str, turns: list[dict[str, str]]) -> dict[str, Any]:
        t = self._types
        contents = [t.Content(role=turn["role"], parts=[t.Part(text=turn["text"])]) for turn in turns]
        config = t.GenerateContentConfig(system_instruction=system, temperature=self.temperature,
                                         response_mime_type="application/json", max_output_tokens=4096)
        last: Exception | None = None
        # Try the chosen model first; if it is overloaded (503/429) or retired (404), fall back down the list.
        chain = [self.model] + [m for m in FALLBACK_CHAIN if m != self.model]
        dead: set[str] = set()
        for round_no in range(ROUNDS):
            if round_no:
                time.sleep(ROUND_WAIT_S * round_no)
            for model in chain:
                if model in dead:
                    continue
                result = self._try(model, contents, config, dead)
                if result is not None:
                    return result
                last = self._last
        raise LLMError(f"Gemini is busy or unavailable on every model ({', '.join(chain)}): {str(last)[:300]}")

    def _try(self, model, contents, config, dead):
        """One model, up to 2 attempts. Returns parsed JSON, or None to move on."""
        self._last = None
        for attempt in range(2):
            try:
                resp = self._client.models.generate_content(model=model, contents=contents, config=config)
                if model != self.model:
                    self.model = model  # remember the model that actually answers
                return _parse_json(resp.text or "")
            except LLMError as exc:  # unparseable reply: retry once, same model
                self._last = exc
            except Exception as exc:
                self._last = exc
                msg = str(exc)
                if any(c in msg for c in ("401", "403", "API key", "PERMISSION_DENIED")):
                    raise LLMError(f"Gemini rejected the key: {msg[:300]}") from exc
                if any(c in msg for c in ("404", "NOT_FOUND")):
                    dead.add(model)  # retired / not available for this key
                    return None
                if any(c in msg for c in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")):
                    if attempt == 0:
                        time.sleep(2)
                        continue
                    return None  # still busy: next model
                time.sleep(1)
        return None
