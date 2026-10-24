"""Records an agent's steps as canonical TraceEvents while it runs."""

from __future__ import annotations

import inspect
import json
import os
from collections.abc import Callable
from typing import Any

from bifura.schemas.models import EventType, TraceEvent


def _jsonable(value: Any) -> Any:
    """Coerce values into JSON-safe data so events validate and serialize."""
    try:
        json.dumps(value)
        return value
    except TypeError:
        if isinstance(value, dict):
            return {str(k): _jsonable(v) for k, v in value.items()}
        if isinstance(value, (list, tuple, set)):
            return [_jsonable(v) for v in value]
        return repr(value)


def _source_location(fn: Callable[..., Any]) -> str | None:
    try:
        path = inspect.getsourcefile(fn)
        _, line = inspect.getsourcelines(fn)
    except (OSError, TypeError):
        return None
    return f"{os.path.basename(path or '?')}:{line}"


class Tracer:
    """Collects TraceEvents for one run.

    Each recording method returns the new event id so later steps can declare the
    data they consume (``deps``). Those declared dependencies become the recorded
    (solid) edges of the impact graph.
    """

    def __init__(self, run_id: str) -> None:
        self.run_id = run_id
        self.events: list[TraceEvent] = []

    # -- low level -------------------------------------------------------
    def _add(self, event_type: EventType, *, name: str, actor: str = "agent",
             kind: str | None = None, deps: list[str] | None = None, **fields: Any) -> str:
        seq = len(self.events) + 1
        event_id = f"e{seq:02d}"
        deps = [d for d in (deps or []) if d]
        for key in ("input_data", "output_data", "state_delta"):
            if fields.get(key) is not None:
                fields[key] = _jsonable(fields[key])
        metadata = dict(fields.pop("metadata", {}) or {})
        if kind:
            metadata["kind"] = kind
        self.events.append(TraceEvent(
            run_id=self.run_id,
            event_id=event_id,
            sequence=seq,
            event_type=event_type.value,
            parent_event_id=self.events[-1].event_id if self.events else None,
            actor=actor,
            name=name,
            depends_on_event_ids=deps,
            data_dependencies=deps,
            metadata=metadata,
            **fields,
        ))
        return event_id

    # -- public API used by the agent under test --------------------------
    def task(self, text: str, expected: str | None = None) -> str:
        return self._add(EventType.TASK_STARTED, name="Task", actor="user", kind="task",
                         summary=text, input_data={"task": text},
                         output_data={"expected": expected} if expected else None,
                         provenance="user_task")

    def decision(self, name: str, output: dict[str, Any], deps: list[str] | None = None,
                 summary: str | None = None, source: Callable[..., Any] | None = None) -> str:
        return self._add(EventType.STATE_UPDATED, name=name, kind="decision", deps=deps,
                         summary=summary or ", ".join(f"{k}={v}" for k, v in output.items()),
                         output_data=output, provenance="agent",
                         source_location=_source_location(source) if source else None)

    def state(self, delta: dict[str, Any], deps: list[str] | None = None, name: str = "State update") -> str:
        return self._add(EventType.STATE_UPDATED, name=name, kind="state", deps=deps,
                         summary=", ".join(f"{k} = {v}" for k, v in delta.items()),
                         input_data=delta, state_delta=delta, provenance="agent")

    def tool(self, name: str, fn: Callable[..., Any], args: dict[str, Any],
             deps: list[str] | None = None, kind: str = "tool call",
             summarize: Callable[[Any], str] | None = None) -> tuple[Any, str]:
        """Run ``fn(**args)`` and record it. Exceptions are recorded, then re-raised."""
        loc = _source_location(fn)
        try:
            result = fn(**args)
        except Exception as exc:  # recorded as an error event, then propagated
            self._add(EventType.ERROR, name=name, actor="tool", kind=kind, deps=deps,
                      tool_name=name, input_data=args, status="failure",
                      error=str(exc), error_type=type(exc).__name__,
                      summary=f"{type(exc).__name__}: {exc}", source_location=loc,
                      provenance="tool")
            raise
        out = result if isinstance(result, dict) else {"result": result}
        event_id = self._add(EventType.TOOL_COMPLETED, name=name, actor="tool", kind=kind,
                             deps=deps, tool_name=name, input_data=args, output_data=out,
                             summary=summarize(result) if summarize else str(result)[:60],
                             status="success", source_location=loc, provenance="tool")
        return result, event_id

    def check(self, name: str, passed: bool, detail: str, deps: list[str] | None = None,
              rule: str | None = None) -> str:
        return self._add(EventType.ASSERTION_PASSED if passed else EventType.ASSERTION_FAILED,
                         name=name, actor="evaluator", kind="assertion", deps=deps,
                         summary=rule or name, input_data={"rule": rule} if rule else None,
                         output_data={"verdict": "passed" if passed else "FAILED", "detail": detail},
                         status="success" if passed else "failure", assertions=[name],
                         provenance="evaluator")

    def finish(self, output: dict[str, Any], deps: list[str] | None = None) -> str:
        return self._add(EventType.RUN_FINISHED, name="Final report", kind="output", deps=deps,
                         summary=str(next(iter(output.values()), ""))[:60], output_data=output,
                         provenance="agent")
