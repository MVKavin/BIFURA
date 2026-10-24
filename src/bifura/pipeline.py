"""End-to-end live investigation: run the agent, investigate, verify, record, learn.

    python -m bifura.pipeline revenue_separator          # uses Gemini if GEMINI_API_KEY is set
    python -m bifura.pipeline growth_args --scripted     # force scripted mode
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bifura.agent.graph import run_workflow
from bifura.agent.session import InvestigationSession
from bifura.analysis.deviation import evaluate_expectations, find_first_deviation
from bifura.analysis.impact_graph import build_impact_graph, downstream_of
from bifura.learning.features import extract_features
from bifura.learning.incident_store import save_incident
from bifura.learning.predict import current_model, predict_failure
from bifura.learning.retrieve import retrieve_similar
from bifura.llm import get_llm, llm_status
from bifura.repair.verification import unified_diff
from bifura.schemas.bundle import RunBundle
from bifura.schemas.models import (
    ExecutionStatus,
    FailureCategory,
    IncidentRecord,
    LabelStatus,
    RunRecord,
    RunStatus,
    VerificationReport,
)
from bifura.tracing.runner import DATA_DIR, REPO_ROOT, apply_fault_env, load_faults, load_scenarios, prepare_workspace, run_agent

RUNS = DATA_DIR / "runs"
INVESTIGATIONS = REPO_ROOT / "results" / "investigations"
PATCHES = REPO_ROOT / "patches"


def new_run_id() -> str:
    return "R-" + datetime.now().strftime("%m%d-%H%M%S")


def capture(scenario_id: str, run_id: str, progress: Callable[[str], None]) -> InvestigationSession:
    scenario = load_scenarios()[scenario_id]
    fault = load_faults()[scenario["fault"]]
    env = apply_fault_env(scenario["env"], fault)
    progress(f"Running the practice agent ({scenario['title']}) with Bifura tracing attached…")
    ws = prepare_workspace(run_id, fault, env)
    run = evaluate_expectations(run_agent(ws, env, run_id), env)
    deviation = find_first_deviation(run, env)
    progress(f"Captured {len(run.events)} events. First deviation: {deviation.description}")
    features = extract_features(run.events, deviation)
    matches = retrieve_similar(run_id, features)
    prediction = predict_failure(run_id, features, [m.incident_id for m in matches[:2]])
    progress(f"Prediction ({prediction.model_version}): " + ", ".join(
        f"{c['category']} {c['score']}" for c in prediction.candidates[:2]))
    return InvestigationSession(run_id=run_id, scenario=scenario, fault=fault, env=env, workspace=ws,
                                original_source=(ws / "agent.py").read_text(encoding="utf-8"), run=run,
                                deviation=deviation, features=features, prediction=prediction, matches=matches,
                                progress=progress)


def _category(value: Any) -> FailureCategory:
    try:
        return FailureCategory(str(value))
    except ValueError:
        return FailureCategory.UNKNOWN_INSUFFICIENT_EVIDENCE


def finalize(s: InvestigationSession) -> dict[str, Any]:
    run_id, events, d = s.run_id, s.run.events, s.deviation
    diag = s.diagnosis or {}
    tests, rp = s.tests_after or {}, s.replay_after or {}
    passed = bool(s.patches) and bool(tests.get("ok")) and bool(rp.get("ok"))
    downstream = downstream_of(events, d.first_deviation_event_id)

    suspect = None
    if s.patches:
        p = s.patches[0]
        suspect = {"label": f"{p['path']}:{p['line']}", "sub": "fix verified" if passed else "suspected location",
                   "detail": diag.get("root_cause") or p.get("hypothesis") or "patched line",
                   "status": "confirmed by replay" if passed else "hypothesis",
                   "why": f"Investigation hypothesis from {s.mode}: {diag.get('root_cause', 'see diagnosis')}."
                          + (" Confirmed: tests and replay pass after this change." if passed else " Not verified.")}
    graph = build_impact_graph(run_id, events, d.first_deviation_event_id, suspect)

    logged = []
    for dec, res in zip(s.decisions, s.results):
        status = dec.execution_status
        if res.executed:
            status = ExecutionStatus.EXECUTED if res.success else ExecutionStatus.EXECUTION_FAILED
        logged.append(dec.model_copy(update={"execution_status": status}))  # audit-log copy; original untouched

    diff = "".join(unified_diff(s.original_source, (s.workspace / "agent.py").read_text(encoding="utf-8")))
    if diff:
        PATCHES.mkdir(parents=True, exist_ok=True)
        (PATCHES / f"{run_id}.diff").write_text(diff, encoding="utf-8")

    total = int(tests.get("passed", 0)) + int(tests.get("failed", 0))
    verification = VerificationReport(
        report_id=f"rep-{run_id}", run_id=run_id, patch_id=f"patch-{run_id}" if s.patches else None, passed=passed,
        total=total, failures=int(tests.get("failed", 0)) + int(tests.get("errors", 0)),
        command="python -m pytest -q test_agent.py  &&  replay " + run_id,
        targeted_test_status="passed" if tests.get("ok") else "failed",
        regression_test_status="passed" if tests.get("ok") else "failed",
        replay_status="passed" if rp.get("ok") else "failed", baseline_run_id=run_id,
        corrected_run_id=f"{run_id}-replay",
        summary=(f"Fixed: tests pass ({tests.get('passed', 0)}/{total}) and replay gives growth {rp.get('growth')}%."
                 if passed else ("No code change was made; " if not s.patches else "Fix not verified; ")
                 + f"replay: {rp.get('deviation') or rp.get('error') or 'n/a'}."))

    category = _category(diag.get("failure_category"))
    incident = IncidentRecord(
        incident_id=f"INC-{run_id}", run_id=run_id, source_run_id=run_id, task_summary=s.scenario["title"],
        observed_pattern=d.description, expected_behavior=d.expected_behavior, observed_behavior=d.observed_behavior,
        first_deviation_event_id=d.first_deviation_event_id, failure_category=category,
        label_status=LabelStatus.VERIFIED if passed else LabelStatus.SUSPECTED,
        root_cause_status="verified" if passed else "suspected", root_cause_summary=diag.get("root_cause"),
        root_cause_hypotheses=[st.hypothesis.get("statement", "") for st in s.steps if st.hypothesis][-3:],
        verified_root_cause=diag.get("root_cause") if passed else None,
        evidence_refs=[str(x) for x in diag.get("evidence", [])][:8], affected_event_ids=downstream,
        downstream_event_ids=downstream, fix_ref=f"patches/{run_id}.diff" if diff else None,
        verified_correction=diag.get("fix") if passed else None, test_refs=["test_agent.py"],
        replay_status="passed" if rp.get("ok") else "failed", data_origin="real_local_run",
        provenance=f"investigated by {s.mode}", training_eligible=False, training_eligibility="pending_review",
        review_status="pending", dataset_version=current_model()[1])
    save_incident(incident, {"text": s.features["text"], "family": s.fault["id"]})

    report = (s.run.state or {}).get("report")
    bundle = RunBundle(
        scenario_id=f"live-{run_id}",
        run=RunRecord(run_id=run_id, task_text=s.env["task"], task_summary=s.scenario["title"],
                      expected_outcome=s.env.get("expected_text"), expected_behavior=json.dumps(s.env["expected"]),
                      actual_behavior=report or s.run.error, status=RunStatus.FAILED,
                      started_at=events[0].timestamp if events else datetime.now(timezone.utc),
                      finished_at=datetime.now(timezone.utc), llm_provider="gemini" if s.mode == "gemini" else None,
                      llm_model=s.llm_model if s.mode == "gemini" else None, is_fixture=False,
                      raw_trace_ref=f"data/runs/{run_id}.json", event_ids=[e.event_id for e in events],
                      tags=[s.scenario["id"], s.mode]),
        expected_action_sequence=["fetch_page", "extract_revenue", "calc_growth", "write_report"],
        actual_execution_summary=report or f"Crashed: {s.run.error_type}: {s.run.error}",
        events=events, safety_decisions=logged, execution_results=s.results, deviation=d,
        incident_matches=s.matches, incident_records=[incident], prediction=s.prediction,
        impact_graph=graph, verification=verification)

    RUNS.mkdir(parents=True, exist_ok=True)
    (RUNS / f"{run_id}.json").write_text(bundle.model_dump_json(indent=2), encoding="utf-8")

    replay_run = rp.get("run")
    transcript = {
        "run_id": run_id, "scenario": s.scenario["id"], "mode": s.mode, "llm_model": s.llm_model,
        "ground_truth": {"fault": s.fault["id"], "category": s.fault["category"], "title": s.fault["title"]},
        "category_correct": category.value == s.fault["category"],
        "diagnosis": diag, "steps": [asdict(st) for st in s.steps], "patches": s.patches, "diff": diff,
        "tests_before": s.tests_before, "tests_after": tests,
        "replay": {k: v for k, v in rp.items() if k != "run"},
        "replay_events": {e.event_id: {"name": e.name, "summary": e.summary} for e in (replay_run.events if replay_run else [])},
        "verified": passed, "notes": s.notes, "original_source": s.original_source,
    }
    INVESTIGATIONS.mkdir(parents=True, exist_ok=True)
    (INVESTIGATIONS / f"{run_id}.json").write_text(json.dumps(transcript, ensure_ascii=False, indent=2, default=str),
                                                   encoding="utf-8")
    s.progress(("✓ Verified fix. " if passed else "✗ Not verified. ") + verification.summary)
    return {"run_id": run_id, "verified": passed, "bundle_path": str(RUNS / f"{run_id}.json"), "mode": s.mode,
            "model": s.llm_model, "diagnosis": diag, "summary": verification.summary,
            "category_correct": transcript["category_correct"]}


def investigate(scenario_id: str, use_llm: bool = True, progress: Callable[[str], None] = print) -> dict[str, Any]:
    run_id = new_run_id()
    llm = get_llm() if use_llm else None
    s = capture(scenario_id, run_id, progress)
    if llm is not None:
        s.mode, s.llm_model = "gemini", llm.model
        progress(f"Investigator: Gemini ({llm.model})")
    else:
        progress("Investigator: scripted mode (no LLM). " + (llm_status().message if use_llm else ""))
    run_workflow(s, llm)
    if llm is not None and s.mode == "gemini":
        s.llm_model = llm.model  # the model that actually answered (after any fallback)
    elif s.mode == "scripted":
        s.llm_model = None
    return finalize(s)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Run the practice agent and investigate its failure.")
    ap.add_argument("scenario", choices=sorted(load_scenarios()))
    ap.add_argument("--scripted", action="store_true", help="do not call the LLM")
    a = ap.parse_args()
    out = investigate(a.scenario, use_llm=not a.scripted)
    print(json.dumps({k: v for k, v in out.items() if k != "diagnosis"}, indent=2))
