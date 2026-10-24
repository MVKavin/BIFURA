"""Run bundle discovery, loading, and formatting for the Bifura dashboard."""

import json
from pathlib import Path
from typing import Any

from bifura.schemas.bundle import RunBundle
from bifura.schemas.models import (
    EventType,
    FailureCategory,
    SafetyDecisionType,
)


NARRATIVES_DIR = Path(__file__).parent / "narratives"


def load_narrative(scenario_id: str | None) -> dict[str, Any] | None:
    """Return optional presentation notes for a scenario, if the dashboard has any.

    Narratives live in ``bifura/dashboard/narratives/{scenario_id}.json`` and only
    add plain-English wording for the story view. They never add trace data.
    """
    if not scenario_id:
        return None
    path = NARRATIVES_DIR / f"{scenario_id}.json"
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _tag_for_event_type(event_type: Any) -> str:
    """Map a trace event type to the node tag shown on the graph."""
    if event_type == EventType.TASK_STARTED:
        return "task"
    if event_type == EventType.TOOL_PROPOSED:
        return "proposal"
    if event_type == EventType.SAFETY_DECISION:
        return "policy"
    if event_type == EventType.TOOL_BLOCKED:
        return "blocked"
    if event_type in (EventType.TOOL_STARTED, EventType.TOOL_COMPLETED):
        return "tool call"
    if event_type == EventType.STATE_UPDATED:
        return "state"
    if event_type in (EventType.ASSERTION_PASSED, EventType.ASSERTION_FAILED):
        return "assertion"
    if event_type == EventType.RUN_FINISHED:
        return "output"
    return "event"


def load_run_bundle(source: str | Path | dict[str, Any]) -> RunBundle:
    """Load and validate a single RunBundle from a path or dict."""
    if isinstance(source, (str, Path)):
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"Run bundle not found at {path}")
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = source
    return RunBundle.model_validate(data)


def load_all_bundles(
    fixtures_dir: str | Path = "data/fixtures",
    runs_dir: str | Path = "data/runs",
) -> dict[str, RunBundle]:
    """Scan and load run bundles from both fixtures and runtime directories.

    Per shared integration contract:
    Dashboard scans data/fixtures/ (tracked) and data/runs/ (runtime).
    """
    bundles: dict[str, RunBundle] = {}

    for dir_path in [Path(fixtures_dir), Path(runs_dir)]:
        if not dir_path.exists():
            continue
        for file in dir_path.glob("*.json"):
            try:
                bundle = load_run_bundle(file)
                key = bundle.scenario_id or bundle.run.run_id
                bundles[key] = bundle
            except Exception:
                # Skip non-RunBundle JSON files (such as raw lists or configs)
                continue

    return bundles


def _text(value: Any) -> str:
    """Render enum members as their value and everything else as a string."""
    return str(getattr(value, "value", value))


def _json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def format_bundle_for_ui(bundle: RunBundle) -> dict[str, Any]:
    """Transform a canonical RunBundle into the UI presentation payload.

    Extracts:
    - Task, expected outcome, actual outcome
    - Graph nodes & causal edges
    - Multi-step investigation timeline
    - Prediction & historical incident matches
    - Policy evaluation & safety decisions
    - Verification & replay results

    The payload feeds ``templates/investigation.html``. Node keys are short
    because the template uses them directly: ``l`` label, ``sub`` subtitle,
    ``in``/``o`` input/output, ``st`` state note, ``et`` trace event type.
    Edge keys: ``s``/``t`` source/target, ``k`` kind, ``inf`` inferred, ``ev`` explanation.
    """
    run = bundle.run
    deviation = bundle.deviation
    prediction = bundle.prediction
    matches = bundle.incident_matches or []
    decisions = bundle.safety_decisions
    events = bundle.events
    events_by_id = {ev.event_id: ev for ev in events if ev.event_id}

    # Task brief details
    task_text = run.task_text or "Execute multi-step agent task"
    expected_text = run.expected_outcome or "Expected behavior satisfied without deviation"
    got_text = bundle.actual_execution_summary or f"Run finished with status: {_text(run.status)}"

    nodes_data: list[dict[str, Any]] = []
    edges_data: list[dict[str, Any]] = []

    if bundle.impact_graph and bundle.impact_graph.nodes:
        # Use the explicit impact graph provided in the bundle. The dashboard
        # only visualizes supplied edges; it never invents causal links.
        count = len(bundle.impact_graph.nodes)
        for idx, n in enumerate(bundle.impact_graph.nodes):
            node_id = n.get("id", f"n{idx+1}")
            ev = events_by_id.get(node_id)
            event_type = _text(ev.event_type) if ev else None
            sub = n.get("sub") or (ev.summary if ev and ev.summary else "")
            nodes_data.append({
                "i": idx,
                "id": node_id,
                "tag": n.get("tag") or (_tag_for_event_type(ev.event_type) if ev else "event"),
                "l": n.get("label") or (ev.name if ev and ev.name else node_id),
                "sub": str(sub),
                # Without layout hints, spread nodes evenly across the canvas.
                "x": n.get("x", 80 + idx * (840 / max(1, count - 1)) if count > 1 else 475),
                "y": n.get("y", 295),
                "in": str(n.get("in") or (_json_text(ev.input_data) if ev and ev.input_data else "—")),
                "o": str(n.get("o") or (_json_text(ev.output_data) if ev and ev.output_data else "—")),
                "st": str(n.get("st") or (_json_text(ev.state_delta) if ev and ev.state_delta else "—")),
                "et": event_type,
            })
        for e in bundle.impact_graph.edges:
            if hasattr(e, "model_dump"):
                ed = e.model_dump(mode="json")
            elif isinstance(e, dict):
                ed = e
            else:
                continue
            edges_data.append({
                "s": ed.get("from_event_id") or ed.get("s"),
                "t": ed.get("to_event_id") or ed.get("t"),
                "k": ed.get("dependency_type") or ed.get("k", "consumes"),
                "inf": 1 if ed.get("evidence_status") == "inferred" or ed.get("inf") else 0,
                "ev": ed.get("explanation") or ed.get("ev"),
            })
    else:
        # Synthesize a visual graph from the trace: task node, then each event
        # linked to its recorded dependencies (or, failing that, its predecessor).
        nodes_data.append({
            "i": 0,
            "id": "task",
            "tag": "task",
            "l": "Task",
            "sub": run.task_summary or "Execute task",
            "x": 80,
            "y": 295,
            "in": task_text,
            "o": "—",
            "st": f"expected: {expected_text}",
            "et": None,
        })
        prev_id = "task"
        for idx, ev in enumerate(events, start=1):
            node_id = ev.event_id or f"n{idx+1}"
            row_y = 190 if idx % 2 == 1 else (400 if idx % 3 == 0 else 295)
            nodes_data.append({
                "i": idx,
                "id": node_id,
                "tag": _tag_for_event_type(ev.event_type),
                "l": ev.name or ev.tool_name or _text(ev.event_type).replace("_", " ").title(),
                "sub": str(ev.summary or ev.tool_name or _text(ev.event_type)),
                "x": min(920, 100 + idx * 135),
                "y": row_y,
                "in": _json_text(ev.input_data) if ev.input_data else (ev.input_ref or "—"),
                "o": _json_text(ev.output_data) if ev.output_data else (ev.output_ref or "—"),
                "st": _json_text(ev.state_delta) if ev.state_delta else "—",
                "et": _text(ev.event_type),
            })
            deps = [d for d in (ev.depends_on_event_ids or ev.data_dependencies or []) if d]
            for dep in deps or [prev_id]:
                edges_data.append({
                    "s": dep,
                    "t": node_id,
                    "k": "depends on" if deps else "leads to",
                    "inf": 0,
                    "ev": None,
                })
            prev_id = node_id

    # Compile the final UI payload
    payload: dict[str, Any] = {
        "scenario_id": bundle.scenario_id,
        "run_id": run.run_id,
        "status": _text(run.status),
        "task_text": task_text,
        "task_summary": run.task_summary,
        "expected_outcome": expected_text,
        "actual_summary": got_text,
        "agent_name": run.agent_name,
        "llm_model": run.llm_model,
        "is_fixture": bool(run.is_fixture),
        "raw_trace_ref": run.raw_trace_ref,
        "started_at": run.started_at.isoformat() if hasattr(run.started_at, "isoformat") else run.started_at,
        "deviation": deviation.model_dump(mode="json") if deviation else None,
        "prediction": prediction.model_dump(mode="json") if prediction else None,
        "incident_matches": [m.model_dump(mode="json") for m in matches],
        "safety_decisions": [d.model_dump(mode="json") for d in decisions],
        "verification": bundle.verification.model_dump(mode="json") if bundle.verification else None,
        "nodes": nodes_data,
        "edges": edges_data,
        "events_count": len(events),
        "event_types": [_text(ev.event_type) for ev in events],
        "raw_events": {ev.event_id: ev.model_dump(mode="json") for ev in events if ev.event_id},
        "policy_status": "enforcing",
        "policy_version": decisions[0].policy_version if decisions else None,
        "narrative": load_narrative(bundle.scenario_id),
        "investigator": None,
    }

    # Live investigations: story text comes from the saved transcript.
    from bifura.dashboard.live import chat_narrative, investigator_name, live_narrative, load_transcript
    transcript = None if run.is_fixture else load_transcript(run.run_id)
    chat = None
    if not run.is_fixture and bundle.scenario_id.startswith("chat-"):
        from bifura.chatcheck.record import load_chat
        chat = load_chat(run.run_id)
    if chat:
        payload["narrative"] = chat_narrative(chat)
        payload["investigator"] = {"name": f"{chat['label']} chat", "mode": "chat", "model": chat.get("model"),
                                   "verified": chat.get("verified")}
    elif transcript:
        payload["narrative"] = live_narrative(transcript, deviation.first_deviation_event_id if deviation else None)
        payload["investigator"] = {"name": investigator_name(transcript), "mode": transcript.get("mode"),
                                   "model": transcript.get("llm_model"), "verified": transcript.get("verified")}

    return payload
