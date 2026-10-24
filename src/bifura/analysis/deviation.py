"""Compare a traced run with its expectations and find the earliest deviation."""

from __future__ import annotations

from typing import Any

from bifura.schemas.models import DeviationRecord, EventType, TraceEvent
from bifura.sdk import Tracer
from bifura.tracing.runner import AgentRun

EXPECTED_SEQUENCE = ["fetch_page", "extract_revenue", "calc_growth", "write_report"]

# Which expected value each recorded field should equal, per tool.
_TOOL_INPUTS = {"fetch_page": {"url": "url"},
                "calc_growth": {"current": "revenue", "previous": "prev_revenue"},
                "write_report": {"growth": "growth"}}
# The practice agent's configured retry budget: 1 attempt + MAX_RETRIES (2) retries.
RETRY_BUDGET = 3
_TOOL_OUTPUTS = {"extract_revenue": "revenue", "calc_growth": "growth"}


def _differs(actual: Any, expected: Any) -> bool:
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)) and not isinstance(actual, bool):
        return abs(actual - expected) > 0.05
    return actual != expected


def evaluate_expectations(run: AgentRun, env: dict[str, Any]) -> AgentRun:
    """Append Bifura's evaluator checks (expected values and step order) to the trace."""
    t = Tracer(run.run_id)
    t.events = run.events
    expected = env["expected"]
    final = next((e.event_id for e in reversed(run.events) if e.event_type == EventType.RUN_FINISHED.value), None)
    last = run.events[-1].event_id if run.events else None
    plan = next((e.event_id for e in run.events if e.name == "Plan"), None)

    if run.crashed:
        t.check("Run completed", False, f"{run.error_type}: {run.error}", deps=[last],
                rule="the agent must finish without an exception")
    else:
        growth = (run.state or {}).get("growth")
        ok = growth is not None and not _differs(growth, expected["growth"])
        t.check("Matches expected growth", ok, f"expected {expected['growth']:+}%, got {growth}",
                deps=[final], rule=f"growth ≈ {expected['growth']:+}%")
        report = (run.state or {}).get("report") or ""
        want = f"{abs(expected['growth'])}%"
        t.check("Report states expected growth", want in report, f"report: {report!r}",
                deps=[final], rule=f"report mentions {want}")

    tools = []
    for e in run.events:
        if e.tool_name and (not tools or tools[-1] != e.tool_name):
            tools.append(e.tool_name)
    t.check("Follows expected step order", tools == EXPECTED_SEQUENCE, " → ".join(tools) or "no tools ran",
            deps=[plan], rule=" → ".join(EXPECTED_SEQUENCE))
    return run


def _first_mismatch(e: TraceEvent, expected: dict[str, Any]) -> tuple[dict, dict] | None:
    """Return (expected, actual) for the first field of this event that is wrong."""
    if e.name == "Plan" and e.output_data:
        plan = e.output_data.get("plan")
        if plan != EXPECTED_SEQUENCE:
            return {"plan": EXPECTED_SEQUENCE}, {"plan": plan}
    if e.tool_name in _TOOL_INPUTS and e.input_data:
        exp, act = {}, {}
        for arg, key in _TOOL_INPUTS[e.tool_name].items():
            if arg in e.input_data and key in expected and _differs(e.input_data[arg], expected[key]):
                exp[arg], act[arg] = expected[key], e.input_data[arg]
        if exp:
            return exp, act
    if e.event_type == EventType.ERROR.value:
        return {"status": "success"}, {"error": f"{e.error_type}: {e.error}"}
    if e.tool_name in _TOOL_OUTPUTS and e.output_data and "result" in e.output_data:
        key = _TOOL_OUTPUTS[e.tool_name]
        if key in expected and _differs(e.output_data["result"], expected[key]):
            return {key: expected[key]}, {key: e.output_data["result"]}
    if e.state_delta:
        for key, value in e.state_delta.items():
            if key in expected and _differs(value, expected[key]):
                return {key: expected[key]}, {key: value}
    return None


def find_first_deviation(run: AgentRun, env: dict[str, Any]) -> DeviationRecord:
    """Earliest event whose recorded input, output or state disagrees with expectations."""
    expected = {"url": env["url"], **env["expected"]}
    for e in run.events:
        hit = _first_mismatch(e, expected)
        if hit:
            exp, act = hit
            where = ("plan" if "plan" in act else "error" if "error" in act
                     else "tool_input" if e.tool_name in _TOOL_INPUTS and set(act) <= set(_TOOL_INPUTS[e.tool_name])
                     else "state" if e.state_delta else "tool_output")
            what = ", ".join(f"{k} = {v}" for k, v in act.items())
            want = ", ".join(f"{k} = {v}" for k, v in exp.items())
            return DeviationRecord(
                run_id=run.run_id, deviation_id=f"dev-{run.run_id}", event_id=e.event_id,
                first_deviation_event_id=e.event_id, found=True, expected=exp, actual=act,
                expected_behavior=f"{e.name} should give {want}",
                observed_behavior=f"{e.name} gave {what}",
                description=f"Step {e.sequence} ({e.name}) gave {what} instead of {want}",
                evidence_refs=[e.event_id] + list(e.data_dependencies), status=f"observed_in_{where}")
    failed = next((e for e in run.events if e.event_type == EventType.ASSERTION_FAILED.value), None)
    if failed:
        return DeviationRecord(run_id=run.run_id, deviation_id=f"dev-{run.run_id}", event_id=failed.event_id,
                               first_deviation_event_id=failed.event_id, found=True,
                               description=f"Check failed: {failed.name}", evidence_refs=[failed.event_id],
                               status="observed")
    return DeviationRecord(run_id=run.run_id, deviation_id=f"dev-{run.run_id}", found=False,
                           description="No deviation from expected behavior", status="observed")
