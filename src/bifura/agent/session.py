"""State of one investigation, and the tool implementations it can (safely) use."""

from __future__ import annotations

import json
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from bifura.schemas.models import (
    DeviationRecord,
    IncidentMatch,
    PredictionResult,
    SafetyDecisionRecord,
    SafetyDecisionType,
    ToolCallProposal,
    ToolExecutionResult,
)
from bifura.tools.executor import execute_tool_action
from bifura.tools.registry import TOOLS
from bifura.tracing.runner import AgentRun, inject
from bifura.repair.verification import replay, run_targeted_tests


def _clip(value: Any, n: int = 2500) -> str:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, default=str)
    return text if len(text) <= n else text[:n] + " …(truncated)"


@dataclass
class Step:
    n: int
    actor: str            # "gemini", "scripted", "orchestrator", "policy check"
    action: str
    args: dict[str, Any]
    thought: str = ""
    hypothesis: dict[str, Any] | None = None
    decision: str | None = None
    rule: str | None = None
    reason: str | None = None
    executed: bool = False
    ok: bool | None = None
    observation: str = ""


@dataclass
class InvestigationSession:
    run_id: str
    scenario: dict[str, Any]
    fault: dict[str, Any]
    env: dict[str, Any]
    workspace: Path
    original_source: str
    run: AgentRun
    deviation: DeviationRecord
    features: dict[str, Any]
    prediction: PredictionResult
    matches: list[IncidentMatch]
    mode: str = "scripted"            # "gemini" or "scripted"
    llm_model: str | None = None
    max_calls: int = 14
    progress: Callable[[str], None] = lambda msg: None
    steps: list[Step] = field(default_factory=list)
    decisions: list[SafetyDecisionRecord] = field(default_factory=list)
    results: list[ToolExecutionResult] = field(default_factory=list)
    patches: list[dict[str, Any]] = field(default_factory=list)
    tests_before: dict[str, Any] | None = None
    tests_after: dict[str, Any] | None = None
    replay_after: dict[str, Any] | None = None
    diagnosis: dict[str, Any] | None = None
    turns: list[dict[str, str]] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    agent_calls: int = 0

    # -- policy context: built here (trusted), never taken from the model --------
    def context(self, provenance: str) -> dict[str, Any]:
        return {"workspace_root": str(self.workspace), "sandbox_root": str(self.workspace),
                "allowed_tools": list(TOOLS), "provenance": provenance, "mode": "investigation",
                "permissions": {"allow_network": False, "write_sandbox": True, "write_project": False, "run_tests": True},
                "budget": {"max_calls": self.max_calls, "used": self.agent_calls} if provenance == "agent" else {},
                "session": self}

    def call(self, tool: str, args: dict[str, Any], actor: str, thought: str = "",
             hypothesis: dict[str, Any] | None = None, model_metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        """Propose a tool call, let the safety gate decide, execute only on ALLOW, log it."""
        provenance = "trusted_orchestrator" if actor == "orchestrator" else "agent"
        proposal = ToolCallProposal(proposal_id=f"prop-{uuid.uuid4().hex[:8]}", run_id=self.run_id,
                                    tool_name=str(tool), arguments=args if isinstance(args, dict) else {},
                                    purpose=thought[:200] or None, model_generated_metadata=model_metadata or {})
        decision, result = execute_tool_action(proposal, self.context(provenance), handlers=HANDLERS)
        if actor in ("gemini", "scripted"):
            self.agent_calls += 1
        self.decisions.append(decision)
        self.results.append(result)
        if result.executed and result.success:
            obs: dict[str, Any] = {"ok": True, "result": result.result_data}
        elif result.executed:
            obs = {"ok": False, "error": f"{result.error_type}: {result.error_message}"}
        else:
            obs = {"ok": False, "decision": decision.decision.value, "rule": decision.policy_rule, "reason": decision.reason,
                   "note": "The safety policy did not run this action."}
        step = Step(n=len(self.steps) + 1, actor=actor, action=str(tool), args=proposal.arguments, thought=thought,
                    hypothesis=hypothesis, decision=decision.decision.value, rule=decision.policy_rule,
                    reason=decision.reason, executed=result.executed, ok=bool(result.success),
                    observation=_clip(obs, 600))
        self.steps.append(step)
        icon = {"ALLOW": "✓", "REVIEW": "⏸", "BLOCK": "✗"}[decision.decision.value]
        self.progress(f"{actor}: {tool}({_args_short(proposal.arguments)}) → {icon} {decision.decision.value}")
        return obs


def _args_short(args: dict[str, Any]) -> str:
    parts = []
    for k, v in args.items():
        s = str(v).replace("\n", " ")
        parts.append(f"{k}={s[:28] + '…' if len(s) > 28 else s}")
    return ", ".join(parts)


# -- tool implementations (only reachable through execute_tool_action) -----------

def _s(context: dict[str, Any]) -> InvestigationSession:
    return context["session"]


def get_run_summary(args, context):
    s = _s(context)
    return {"task": s.env["task"], "expected": s.env["expected"], "expected_text": s.env.get("expected_text"),
            "status": "failed", "crash": s.run.error and f"{s.run.error_type}: {s.run.error}",
            "first_deviation": s.deviation.model_dump(mode="json", include={"first_deviation_event_id", "description",
                                                                              "expected", "actual"}),
            "events": [{"id": e.event_id, "type": e.event_type, "name": e.name, "summary": e.summary,
                        "depends_on": e.data_dependencies, "source": e.source_location} for e in s.run.events]}


def get_trace_event(args, context):
    s = _s(context)
    ev = next((e for e in s.run.events if e.event_id == args["event_id"]), None)
    if ev is None:
        raise KeyError(f"no event {args['event_id']}; ids are " + ", ".join(e.event_id for e in s.run.events))
    return ev.model_dump(mode="json", exclude={"schema_version", "run_id", "timestamp", "parent_event_id"})


def inspect_source_file(args, context):
    s = _s(context)
    path = (s.workspace / args["path"]).resolve()
    lines = path.read_text(encoding="utf-8").splitlines()
    start = max(1, int(args.get("start_line") or 1))
    end = min(len(lines), int(args.get("end_line") or start + 79), start + 119)
    return {"path": args["path"], "lines": f"{start}-{end} of {len(lines)}",
            "text": "\n".join(f"{i:>3}| {lines[i - 1]}" for i in range(start, end + 1))}


def search_source(args, context):
    s = _s(context)
    hits = []
    for name in ("agent.py", "test_agent.py"):
        for i, line in enumerate((s.workspace / name).read_text(encoding="utf-8").splitlines(), 1):
            if args["query"] in line:
                hits.append(f"{name}:{i}: {line.strip()}")
    return {"query": args["query"], "matches": hits[:30]}


def get_prediction(args, context):
    p = _s(context).prediction
    return {"model_version": p.model_version, "dataset_version": p.dataset_version, "mode": p.prediction_mode,
            "ranked": p.candidates, "score_meaning": p.score_meaning,
            "note": "A prediction is a hypothesis to check, not a verified cause."}


def retrieve_incidents(args, context):
    return {"matches": [m.model_dump(mode="json", include={"incident_id", "similarity_score", "match_reason",
                                                           "matched_features", "verified"}) for m in _s(context).matches]}


def create_candidate_patch(args, context):
    s = _s(context)
    path = (s.workspace / args["path"]).resolve()
    before = path.read_text(encoding="utf-8")
    old, new = args["old"], args["new"]
    if old == new:
        raise ValueError("old and new are identical")
    if before.count(old) != 1:
        raise ValueError(f"'old' must match exactly one place in {args['path']} (found {before.count(old)}). "
                         "Copy it exactly from inspect_source_file output, without the line-number prefix.")
    line = before[: before.index(old)].count("\n") + 1
    path.write_text(inject(before, [{"old": old, "new": new}]), encoding="utf-8")
    s.patches.append({"path": args["path"], "old": old, "new": new, "line": line,
                      "hypothesis": args.get("hypothesis", "")})
    return {"patched": args["path"], "line": line, "note": "Applied in the sandbox copy only."}


def run_targeted_test(args, context):
    s = _s(context)
    res = run_targeted_tests(s.workspace)
    return {k: res[k] for k in ("passed", "failed", "errors", "ok", "summary", "failures")}


def replay_run(args, context):
    s = _s(context)
    r = replay(s.workspace, f"{s.run_id}-replay")
    s.replay_after = r
    return {k: r[k] for k in ("ok", "growth", "report", "error", "checks", "deviation")}


HANDLERS = {"get_run_summary": get_run_summary, "get_trace_event": get_trace_event,
            "inspect_source_file": inspect_source_file, "search_source": search_source,
            "get_prediction": get_prediction, "retrieve_incidents": retrieve_incidents,
            "create_candidate_patch": create_candidate_patch, "run_targeted_test": run_targeted_test,
            "replay_run": replay_run}

assert set(HANDLERS) == set(TOOLS), "every registered tool needs exactly one handler"
_ = SafetyDecisionType  # re-exported for callers that inspect decisions
