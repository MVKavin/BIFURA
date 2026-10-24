"""Read LLM settings from the environment / .env (never from source code).

Providers: gemini (GEMINI_API_KEY), gpt (OPENAI_API_KEY), claude (ANTHROPIC_API_KEY).
Optional model overrides: LLM_MODEL (Gemini), OPENAI_MODEL, CLAUDE_MODEL.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

from bifura.llm.base import LLMClient, LLMError, LLMStatus
from bifura.tracing.runner import REPO_ROOT

load_dotenv(REPO_ROOT / ".env")

PROVIDERS = {
    "gemini": {"label": "Gemini (Google)", "keys": ("GEMINI_API_KEY", "GOOGLE_API_KEY", "LLM_API_KEY"),
               "model_env": "LLM_MODEL", "package": "google.genai"},
    "gpt": {"label": "GPT (OpenAI)", "keys": ("OPENAI_API_KEY",), "model_env": "OPENAI_MODEL", "package": "openai"},
    "claude": {"label": "Claude (Anthropic)", "keys": ("ANTHROPIC_API_KEY",), "model_env": "CLAUDE_MODEL",
               "package": "anthropic"},
}


def _key(provider: str = "gemini") -> str | None:
    for name in PROVIDERS[provider]["keys"]:
        if os.environ.get(name):
            return os.environ[name]
    return None


def provider_status(provider: str) -> LLMStatus:
    load_dotenv(REPO_ROOT / ".env", override=True)
    spec = PROVIDERS[provider]
    model = os.environ.get(spec["model_env"]) or None
    if not _key(provider):
        return LLMStatus(provider, model, False, f"No {spec['keys'][0]} in .env.")
    try:
        __import__(spec["package"])
    except ImportError:
        return LLMStatus(provider, model, False, f"Key found, but the SDK is missing: pip install {spec['package'].split('.')[0]}"
                         + ("" if provider != "gemini" else "-genai"))
    return LLMStatus(provider, model, True, f"{spec['label']} key found.")


def llm_status() -> LLMStatus:
    """Status of the investigator LLM (Gemini; LLM_PROVIDER may pick another)."""
    load_dotenv(REPO_ROOT / ".env", override=True)
    provider = (os.environ.get("LLM_PROVIDER") or "gemini").lower()
    if provider not in PROVIDERS:
        return LLMStatus(provider, None, False, f"Unknown LLM_PROVIDER={provider}; use gemini, gpt or claude.")
    status = provider_status(provider)
    if not status.ready and provider == "gemini":
        status.message = "No GEMINI_API_KEY in .env. Investigations run in scripted mode."
    return status


def get_llm(provider: str | None = None) -> LLMClient | None:
    """A ready client for ``provider`` (default: LLM_PROVIDER or gemini), or None if not configured."""
    load_dotenv(REPO_ROOT / ".env", override=True)
    provider = (provider or os.environ.get("LLM_PROVIDER") or "gemini").lower()
    status = provider_status(provider) if provider in PROVIDERS else None
    if status is None or not status.ready:
        return None
    try:
        if provider == "gemini":
            from bifura.llm.gemini import GeminiClient
            return GeminiClient(api_key=_key("gemini"), model=status.model)
        if provider == "gpt":
            from bifura.llm.openai_client import OpenAIClient
            return OpenAIClient(api_key=_key("gpt"), model=status.model)
        from bifura.llm.claude import ClaudeClient
        return ClaudeClient(api_key=_key("claude"), model=status.model)
    except LLMError:
        return None
