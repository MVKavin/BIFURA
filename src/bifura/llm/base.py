"""Provider-neutral interface for the investigation LLM."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


class LLMError(RuntimeError):
    """The provider failed (network, quota, auth, invalid output)."""


@dataclass
class LLMStatus:
    provider: str
    model: str | None
    ready: bool
    message: str


class LLMClient(Protocol):
    provider: str
    model: str

    def next_json(self, system: str, turns: list[dict[str, str]]) -> dict[str, Any]:
        """Return the model's next reply parsed as a JSON object.

        ``turns`` alternate ``{"role": "user"|"model", "text": ...}``.
        """
        ...
