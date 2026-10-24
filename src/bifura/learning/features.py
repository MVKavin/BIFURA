"""Turn a traced run into features for the failure-category model.

Features only use what Bifura observes in the trace and the expectation checks.
They never include the injected fault id or its category (no label leakage).
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from bifura.analysis.deviation import RETRY_BUDGET
from bifura.schemas.models import DeviationRecord, EventType, TraceEvent


def _ratio_token(actual: Any, expected: Any) -> str | None:
    if not isinstance(actual, (int, float)) or not isinstance(expected, (int, float)) or isinstance(actual, bool):
        return None
    if expected == 0:
        return "ratio_zero_expected"
    r = actual / expected
    if r < 0:
        return "ratio_sign_flip"
    for lo, hi, name in [(0, 0.002, "ratio_tiny"), (0.002, 0.2, "ratio_div_10_1000"), (0.2, 0.95, "ratio_lower"),
                         (0.95, 1.05, "ratio_close"), (1.05, 5, "ratio_higher"), (5, float("inf"), "ratio_x_10_1000")]:
        if lo <= r < hi:
            return name
    return None


def extract_features(events: list[TraceEvent], deviation: DeviationRecord | None) -> dict[str, Any]:
    """Return ``{"text": <token string>, ...structured counts}`` for one run."""
    tokens: list[str] = []
    types = [e.event_type for e in events]
    tokens += [f"evt_{t}" for t in types]
    tools = [e.tool_name for e in events if e.tool_name]
    tokens += [f"tool_{t}" for t in tools]
    errors = [e for e in events if e.event_type == EventType.ERROR.value]
    tokens += [f"err_{e.error_type}" for e in errors]
    tokens += [f"errtool_{e.tool_name}_{e.error_type}" for e in errors]
    failed = [e.name for e in events if e.event_type == EventType.ASSERTION_FAILED.value]
    tokens += ["fail_" + n.lower().replace(" ", "_") for n in failed]

    repeats = Counter((e.tool_name, e.error_type) for e in errors)
    max_repeat = max(repeats.values(), default=0)
    tokens.append(f"err_repeat_{min(max_repeat, 4)}")
    if errors:
        tokens.append("err_repeat_over_budget" if max_repeat > RETRY_BUDGET else "err_within_retry_budget")
        tokens.append("err_retried" if max_repeat > 1 else "err_not_retried")
    tokens.append(f"n_errors_{min(len(errors), 4)}")
    if not any(e.event_type == EventType.RUN_FINISHED.value for e in events):
        tokens.append("run_unfinished")

    if deviation and deviation.found:
        if deviation.status.startswith("observed_in_"):
            tokens.append("dev_in_" + deviation.status.removeprefix("observed_in_"))
        dev = next((e for e in events if e.event_id == deviation.first_deviation_event_id), None)
        if dev is not None:
            tokens.append(f"dev_kind_{dev.metadata.get('kind', 'event')}")
            tokens.append(f"dev_type_{dev.event_type}")
            if dev.tool_name:
                tokens.append(f"dev_tool_{dev.tool_name}")
            tokens.append("dev_first_event" if dev.sequence <= 2 else "dev_later_event")
        exp, act = deviation.expected or {}, deviation.actual or {}
        for key in act:
            tokens.append(f"dev_field_{key}")
            tok = _ratio_token(act.get(key), exp.get(key))
            if tok:
                tokens.append(tok)
        if set(exp) == set(act) and len(exp) >= 2 and sorted(map(str, exp.values())) == sorted(map(str, act.values())):
            tokens.append("dev_values_swapped")
        if "plan" in act:
            plan, want = act.get("plan") or [], exp.get("plan") or []
            tokens.append("plan_missing_step" if len(plan) < len(want) else "plan_reordered")
        if any(isinstance(v, str) and not isinstance(exp.get(k), str) for k, v in act.items() if k != "error"):
            tokens.append("dev_type_mismatch")
    else:
        tokens.append("no_deviation")

    return {"text": " ".join(tokens), "n_events": len(events), "n_errors": len(errors),
            "max_error_repeat": max_repeat, "n_failed_checks": len(failed)}
