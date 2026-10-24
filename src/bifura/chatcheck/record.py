"""Save a chat check as a canonical RunBundle so it plays in the story + graph view."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any

from bifura.analysis.impact_graph import build_impact_graph, downstream_of
from bifura.chatcheck.checker import CheckReport
from bifura.chatcheck.session import ChatRun
from bifura.llm.config import PROVIDERS
from bifura.schemas.bundle import RunBundle
from bifura.schemas.models import DeviationRecord, PredictionResult, RunRecord, RunStatus, VerificationReport
from bifura.sdk import Tracer
from bifura.tracing.runner import DATA_DIR, REPO_ROOT

RUNS = DATA_DIR / "runs"
CHATS = REPO_ROOT / "results" / "chats"


def _trace(run: ChatRun, report: CheckReport, solution: dict[str, Any]) -> tuple[Tracer, dict[str, str], str | None]:
    """Turn the AI's first answer into trace events. Returns (tracer, name -> event id, final event id)."""
    t = Tracer(run.run_id)
    label = PROVIDERS.get(run.provider, {}).get("label", run.provider)
    task = t.task(run.question, run.expected)
    t.events[-1].name = "Question"
    givens_ev = t.decision("Read the numbers", {k: v for k, v in report.givens.items()}, deps=[task],
                           summary=", ".join(f"{k}={v:g}" for k, v in list(report.givens.items())[:4]))
    t.events[-1].actor = "llm"
    where = {k: givens_ev for k in report.givens}
    last = givens_ev
    for st in report.steps:
        deps = sorted({where[u] for u in st.uses if u in where}) or [givens_ev]
        ev = t.decision(st.name, {"value": st.claimed}, deps=deps,
                        summary=f"{st.name} = {st.claimed:g}" if st.claimed is not None else st.name)
        e = t.events[-1]
        e.actor = "llm"
        e.input_data = {"formula": st.formula, "uses": st.uses, "explanation": st.explanation}
        e.metadata["kind"] = "step"
        where[st.name] = last = ev
    answer = str(solution.get("answer_text") or "")[:300]
    final_ev = t.finish({"answer": answer or f"{report.final_name} = {report.final_claimed}"}, deps=[where.get(report.final_name or "", last)])
    t.events[-1].name = f"{label} answer"
    t.check("Bifura recalculation", report.first_wrong is None and not report.given_problems,
            report.first_wrong.note if report.first_wrong else "every step recalculates correctly",
            deps=[final_ev], rule="every formula must give the value written")
    if report.expected_final is not None:
        t.check("Matches expected answer", bool(report.final_matches_expected),
                f"expected {report.expected_final:g}, got {report.final_claimed}", deps=[final_ev],
                rule=f"final ≈ {report.expected_final:g}")
    return t, where, final_ev


def save_chat_run(run: ChatRun) -> dict[str, Any]:
    if not run.first:
        raise ValueError(run.error or "The AI gave no answer to check.")
    first, last = run.first, run.last
    rep = first.report
    t, where, _ = _trace(run, rep, first.solution)
    events = t.events
    label = PROVIDERS.get(run.provider, {}).get("label", run.provider)

    w = rep.first_wrong
    dev_id = where.get(w.name) if w else (where.get(next(iter(rep.givens), "")) if rep.given_problems else None)
    if w:
        deviation = DeviationRecord(
            run_id=run.run_id, deviation_id=f"dev-{run.run_id}", event_id=dev_id, first_deviation_event_id=dev_id,
            found=True, expected={w.name: round(w.recomputed, 6)}, actual={w.name: w.claimed},
            expected_behavior=f"{w.formula} should give {w.recomputed:.6g}",
            observed_behavior=f"The AI wrote {w.name} = {w.claimed:g}",
            description=f"Step {w.n} ({w.name}) gave {w.name} = {w.claimed:g} instead of {w.recomputed:.6g}",
            evidence_refs=[dev_id], status="observed_in_tool_output")
    elif rep.given_problems:
        deviation = DeviationRecord(run_id=run.run_id, deviation_id=f"dev-{run.run_id}", event_id=dev_id,
                                    first_deviation_event_id=dev_id, found=True,
                                    description=rep.given_problems[0], status="observed_in_state")
    else:
        deviation = DeviationRecord(run_id=run.run_id, deviation_id=f"dev-{run.run_id}", found=False,
                                    description="Every step recalculates correctly", status="observed")

    slip = w.mistake_type if w else ("wrong number copied from the question" if rep.given_problems else None)
    prediction = PredictionResult(
        run_id=run.run_id, prediction_id=f"pred-{run.run_id}", model_version="slip-rules-v1", dataset_version="none",
        prediction_mode="rules_baseline", predicted_categories=[slip] if slip else [],
        candidates=[{"category": slip, "score": 1.0, "score_kind": "rule_match"}] if slip else [],
        scores={slip: 1.0} if slip else {}, score_meaning="rule_match_not_a_probability",
        abstained=slip is None, abstention_reason=None if slip else "No calculation mistake to classify.")

    lr = last.report
    total = len(lr.steps)
    bad = sum(s.status in ("wrong", "affected", "unverifiable") for s in lr.steps)
    corrected = len(run.attempts) > 1
    verification = VerificationReport(
        report_id=f"rep-{run.run_id}", run_id=run.run_id, passed=run.verified and corrected, total=total,
        failures=bad, command="Bifura recalculation of every step (SymPy)",
        targeted_test_status="passed" if lr.ok else "failed", regression_test_status="passed" if lr.ok else "failed",
        replay_status="passed" if lr.ok else "failed", baseline_run_id=run.run_id,
        summary=(f"After {len(run.attempts) - 1} correction(s), every one of {total} steps recalculates correctly"
                 + (f" and the answer matches {lr.expected_final:g}." if lr.final_matches_expected else ".")
                 if lr.ok else f"Still wrong after {len(run.attempts) - 1} correction(s): {bad} step(s) do not check out."))

    suspect = None
    if w:
        suspect = {"label": f"Step {w.n}: {w.name}", "sub": "wrong calculation", "detail": w.note,
                   "status": "confirmed by recalculation",
                   "why": f"Bifura recalculated {w.formula} = {w.recomputed:.6g}; the AI wrote {w.claimed:g}."}
    graph = build_impact_graph(run.run_id, events, deviation.first_deviation_event_id, suspect)

    report_line = str(first.solution.get("answer_text") or "")
    bundle = RunBundle(
        scenario_id=f"chat-{run.run_id}",
        run=RunRecord(run_id=run.run_id, task_text=run.question, task_summary=f"Chat check · {label}",
                      expected_outcome=run.expected or "Every step recalculates correctly",
                      actual_behavior=f"{rep.final_name} = {rep.final_claimed}", status=RunStatus.FAILED if not rep.ok else RunStatus.SUCCEEDED,
                      started_at=events[0].timestamp, finished_at=datetime.now(timezone.utc),
                      llm_provider=run.provider, llm_model=run.model, is_fixture=False,
                      raw_trace_ref=f"results/chats/{run.run_id}.json", event_ids=[e.event_id for e in events],
                      tags=["chat", run.provider] + (["demo_slip"] if run.demo_slip else [])),
        actual_execution_summary=f"{label} answered {rep.final_name} = {rep.final_claimed:g}" if rep.final_claimed is not None else report_line[:200],
        events=events, deviation=deviation, prediction=prediction, incident_matches=[], impact_graph=graph,
        verification=verification)
    RUNS.mkdir(parents=True, exist_ok=True)
    (RUNS / f"{run.run_id}.json").write_text(bundle.model_dump_json(indent=2), encoding="utf-8")

    transcript = {
        "run_id": run.run_id, "kind": "chat", "question": run.question, "provider": run.provider, "label": label,
        "model": run.model, "demo_slip": run.demo_slip, "expected": run.expected, "error": run.error,
        "verified": run.verified, "corrected": corrected, "first_deviation_event_id": deviation.first_deviation_event_id,
        "step_events": where, "downstream": downstream_of(events, deviation.first_deviation_event_id),
        "attempts": [{"kind": a.prompt_kind, "solution": a.solution, "ok": a.report.ok,
                      "given_problems": a.report.given_problems,
                      "final": {"name": a.report.final_name, "claimed": a.report.final_claimed, "true": a.report.final_true},
                      "steps": [asdict(s) for s in a.report.steps]} for a in run.attempts],
    }
    CHATS.mkdir(parents=True, exist_ok=True)
    (CHATS / f"{run.run_id}.json").write_text(json.dumps(transcript, ensure_ascii=False, indent=2), encoding="utf-8")
    return transcript


def load_chat(run_id: str) -> dict[str, Any] | None:
    path = CHATS / f"{run_id}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
