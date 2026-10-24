"""Scripted investigator used when no LLM key is configured.

It walks the same tools through the same safety gate, but its decisions are fixed
and its patch is the scenario's known reference fix. Everything it produces is
labelled ``scripted`` in the trace and dashboard; it is not autonomous reasoning.
"""

from __future__ import annotations

from typing import Any

from bifura.agent.session import InvestigationSession


def plan(s: InvestigationSession) -> list[tuple[str, dict[str, Any], str]]:
    dev_id = s.deviation.first_deviation_event_id or s.run.events[-1].event_id
    actions = [("get_run_summary", {}, "Start from the run summary and the recorded first deviation."),
               ("get_trace_event", {"event_id": dev_id}, "Read the event where the first deviation was recorded."),
               ("get_prediction", {}, "Check which failure category the trained model ranks first."),
               ("retrieve_incidents", {}, "Look for similar verified incidents.")]
    source = s.workspace.joinpath("agent.py").read_text(encoding="utf-8")
    for rep in s.fault.get("code") or []:
        line = source[: source.find(rep["new"])].count("\n") + 1
        actions.append(("inspect_source_file", {"path": "agent.py", "start_line": max(1, line - 6), "end_line": line + 6},
                        "Read the code around the suspected line."))
    for rep in s.fault.get("code") or []:
        actions.append(("create_candidate_patch", {"path": "agent.py", "old": rep["new"], "new": rep["old"],
                                                   "hypothesis": s.fault["title"]},
                        "Apply the scenario's reference fix in the sandbox copy (scripted mode)."))
    if s.fault.get("code"):
        actions.append(("run_targeted_test", {}, "Run the agent's tests on the patched copy."))
    return actions


def finish(s: InvestigationSession) -> dict[str, Any]:
    code = bool(s.fault.get("code"))
    loc = f"agent.py:{s.patches[0]['line']}" if s.patches else "environment"
    return {"diagnosis": f"{s.fault['title']}. {s.deviation.description}.",
            "root_cause": f"{loc}: {s.fault['title'].lower()}",
            "failure_category": s.fault["category"],
            "evidence": [s.deviation.first_deviation_event_id or "", loc],
            "fix": "Reverted the faulty line to the reference implementation." if code
                   else "No code change: the failure comes from the environment."}
