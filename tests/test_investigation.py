"""End-to-end investigation tests (no network: the LLM is a scripted fake)."""

import json
import uuid

import pytest

import bifura.learning.incident_store as store
import bifura.pipeline as pipeline
from bifura.agent.graph import run_workflow
from bifura.llm.base import LLMError
from bifura.llm.gemini import _parse_json
from bifura.schemas.bundle import RunBundle


@pytest.fixture(autouse=True)
def isolated_outputs(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, "RUNS", tmp_path / "runs")
    monkeypatch.setattr(pipeline, "INVESTIGATIONS", tmp_path / "inv")
    monkeypatch.setattr(pipeline, "PATCHES", tmp_path / "patches")
    monkeypatch.setattr(store, "INCIDENTS", tmp_path / "incidents")
    return tmp_path


class FakeLLM:
    """Replies like Gemini would: one JSON action per turn."""
    provider, model = "gemini", "fake-gemini"

    def __init__(self, replies):
        self.replies = list(replies)
        self.seen = []

    def next_json(self, system, turns):
        self.seen.append(turns[-1]["text"])
        if not self.replies:
            raise LLMError("out of replies")
        return self.replies.pop(0)


GOOD = [
    {"thought": "Look at the deviating event.", "action": "get_trace_event", "args": {"event_id": "e04"},
     "hypothesis": {"category": "state_or_dataflow", "statement": "extraction is wrong", "confidence": "medium"}},
    {"thought": "Try to read secrets (should be blocked).", "action": "inspect_source_file", "args": {"path": "../../.env"}},
    {"thought": "Read the extractor.", "action": "inspect_source_file", "args": {"path": "agent.py", "start_line": 30, "end_line": 45}},
    {"thought": "Fix the separator handling.", "action": "create_candidate_patch",
     "args": {"path": "agent.py", "old": 'value = int(float(txt.replace(",", ".")) * 100)', "new": 'value = int(txt.replace(",", ""))'}},
    {"thought": "Check.", "action": "run_targeted_test", "args": {}},
    {"thought": "Done.", "action": "finish", "args": {"diagnosis": "The comma was read as a decimal point.",
     "root_cause": "agent.py:38 replaces ',' with '.'", "failure_category": "state_or_dataflow",
     "evidence": ["e04", "agent.py:38"], "fix": "strip separators"}},
]


def run_with(llm, scenario="revenue_separator"):
    run_id = f"T-{uuid.uuid4().hex[:6]}"
    s = pipeline.capture(scenario, run_id, lambda m: None)
    s.mode, s.llm_model = "gemini", llm.model
    run_workflow(s, llm)
    return s, pipeline.finalize(s)


def test_gemini_style_investigation_fixes_and_verifies(isolated_outputs):
    llm = FakeLLM(GOOD)
    s, out = run_with(llm)
    assert out["verified"] and out["category_correct"]
    assert s.tests_before["failed"] > 0 and s.tests_after["ok"]
    blocked = [st for st in s.steps if st.decision == "BLOCK"]
    assert {st.actor for st in blocked} == {"policy check", "gemini"}
    assert all(not st.executed for st in blocked)
    bundle = RunBundle.model_validate_json((isolated_outputs / "runs" / f"{s.run_id}.json").read_text(encoding="utf-8"))
    assert bundle.verification.passed and bundle.incident_records[0].label_status.value == "verified"
    assert any(n["tag"] == "code" for n in bundle.impact_graph.nodes)
    assert "Observation:" in llm.seen[1]  # the model saw the tool result


def test_failed_fix_is_not_reported_as_verified():
    bad = [{"thought": "Wrong fix.", "action": "create_candidate_patch",
            "args": {"path": "agent.py", "old": "MAX_RETRIES = 2", "new": "MAX_RETRIES = 3"}},
           {"thought": "Done.", "action": "finish", "args": {"diagnosis": "guess", "failure_category": "retry_logic"}}]
    s, out = run_with(FakeLLM(bad + bad[1:]))
    assert not out["verified"] and not out["category_correct"]
    inc = json.loads((store.INCIDENTS / f"INC-{s.run_id}.json").read_text(encoding="utf-8"))
    assert inc["label_status"] == "suspected" and inc["training_eligible"] is False


def test_llm_failure_at_start_falls_back_to_scripted():
    s, out = run_with(FakeLLM([]))
    assert s.mode == "scripted" and out["verified"]
    assert any("scripted" in n for n in s.notes)


def test_test_files_cannot_be_patched_by_the_model():
    sneaky = [{"thought": "Make tests pass.", "action": "create_candidate_patch",
               "args": {"path": "test_agent.py", "old": "def test_", "new": "def _skip_"}},
              {"thought": "Done.", "action": "finish", "args": {"diagnosis": "x", "failure_category": "state_or_dataflow"}}]
    s, out = run_with(FakeLLM(sneaky + sneaky[1:]))
    step = next(st for st in s.steps if st.args.get("path") == "test_agent.py")
    assert step.decision == "REVIEW" and not step.executed and not out["verified"]


def test_parse_json_handles_fenced_replies():
    assert _parse_json('```json\n{"action": "finish"}\n```') == {"action": "finish"}
    with pytest.raises(LLMError):
        _parse_json("no json here")
