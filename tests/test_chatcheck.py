"""Chat check: exact step recalculation, correction loop, recording, providers (no network)."""

import pytest

import bifura.chatcheck.record as record
from bifura.chatcheck.checker import check_solution, classify_slip, parse
from bifura.chatcheck.session import DEMO_SLIP, EXAMPLES, run_chat_check
from bifura.dashboard.loader import format_bundle_for_ui, load_run_bundle
from bifura.llm import provider_status
from bifura.llm.base import LLMError

Q = EXAMPLES["Series circuit (current and power)"]
GIVENS = {"V": 12, "R1": 4, "R2": 2}


def sol(i, v1, p, final=None):
    return {"answer_text": "...", "givens": GIVENS, "steps": [
        {"name": "R_total", "formula": "R1 + R2", "value": 6},
        {"name": "I", "formula": "V / R_total", "value": i},
        {"name": "V_R1", "formula": "I * R1", "value": v1},
        {"name": "P_R1", "formula": "I * V_R1", "value": p}],
        "final": {"name": "P_R1", "value": final if final is not None else p}}


BAD, GOOD = sol(3, 12, 36), sol(2, 8, 16)


def test_first_wrong_step_and_inherited_steps():
    r = check_solution(Q, BAD)
    assert r.first_wrong.n == 2 and r.first_wrong.recomputed == pytest.approx(2)
    assert [s.name for s in r.affected] == ["V_R1", "P_R1"]
    assert r.final_true == pytest.approx(16) and not r.ok


def test_correct_solution_passes_and_rounding_is_allowed():
    s = sol(2, 8, 16)
    s["steps"].append({"name": "x", "formula": "2/3", "value": 0.667})  # rounded: still counts as correct
    assert check_solution(Q, s, expected_final="16 W").ok
    assert check_solution(Q, GOOD, expected_final="16 W").ok


def test_expected_answer_catches_a_wrong_formula():
    wrong_formula = sol(2, 8, 4)  # arithmetic fine (I*V_R1 written but value 4) -> flagged as wrong step
    wrong_formula["steps"][3] = {"name": "P_R1", "formula": "V_R1 / I", "value": 4}  # consistent but wrong physics
    r = check_solution(Q, wrong_formula, expected_final="16")
    assert r.first_wrong is None and r.final_matches_expected is False and not r.ok


def test_names_like_I_and_E_are_quantities_not_sympy_constants():
    assert str(parse("I*E + S")) == "E*I + S" and parse("I*E").free_symbols


def test_slip_types():
    vals = {"a": 6.0, "b": 2.0}
    assert classify_slip("a / b", vals, -3, 3) == "sign error"
    assert classify_slip("a / b", vals, 30, 3).startswith("decimal")
    assert classify_slip("a / b", vals, 1 / 3, 3) == "upside-down division"
    assert classify_slip("a - b", vals, 8, 4) == "used '+' instead of '-'"


def test_number_not_in_question_is_flagged():
    s = sol(2, 8, 16)
    s["givens"] = {"V": 12, "R1": 40, "R2": 2}
    assert check_solution(Q, s).given_problems


class FakeLLM:
    model = "fake-model"

    def __init__(self, replies):
        self.replies, self.systems, self.seen = list(replies), [], []

    def next_json(self, system, turns):
        self.systems.append(system)
        self.seen.append(turns[-1]["text"])
        if not self.replies:
            raise LLMError("busy (503)")
        return self.replies.pop(0)


def test_correction_loop_tells_ai_the_exact_problem_and_verifies():
    llm = FakeLLM([BAD, GOOD])
    run = run_chat_check(Q, llm, "gemini", demo_slip=True, expected="16 W")
    assert run.needed_fix and run.verified and len(run.attempts) == 2
    assert "Step 2 (I)" in llm.seen[1] and "gives 2" in llm.seen[1]
    assert DEMO_SLIP in llm.systems[0] and DEMO_SLIP not in llm.systems[1]  # corrections are asked to be right


def test_stays_unverified_when_ai_keeps_failing():
    run = run_chat_check(Q, FakeLLM([BAD, BAD, BAD]), "gemini")
    assert not run.verified and len(run.attempts) == 3


def test_ai_error_is_reported_not_hidden():
    run = run_chat_check(Q, FakeLLM([]), "gemini")
    assert not run.attempts and "busy" in run.error


def test_chat_run_becomes_a_story_view_run(tmp_path, monkeypatch):
    monkeypatch.setattr(record, "RUNS", tmp_path / "runs")
    monkeypatch.setattr(record, "CHATS", tmp_path / "chats")
    run = run_chat_check(Q, FakeLLM([BAD, GOOD]), "gemini", expected="16")
    t = record.save_chat_run(run)
    p = format_bundle_for_ui(load_run_bundle(tmp_path / "runs" / f"{run.run_id}.json"))
    assert p["deviation"]["first_deviation_event_id"] == t["step_events"]["I"]
    assert p["verification"]["passed"] is True
    assert any(n["tag"] == "code" and n["l"] == "Step 2: I" for n in p["nodes"])
    assert p["narrative"]["titles"]["fix"] == "Ask the AI to correct itself"
    assert "<script" not in str(p["narrative"])


def test_missing_provider_keys_are_reported(monkeypatch):
    for k in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
        monkeypatch.setenv(k, "")
    monkeypatch.setattr("bifura.llm.config.load_dotenv", lambda *a, **k: None)
    assert not provider_status("gpt").ready and "OPENAI_API_KEY" in provider_status("gpt").message
    assert not provider_status("claude").ready
