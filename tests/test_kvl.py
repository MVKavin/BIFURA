"""KVL check: derivation with the dot convention, reading messy equations, checking chats/AIs."""

import copy

import pytest

from bifura.dashboard.kvl_page import _from_rows, _rows
from bifura.kvl.ai import ask_ai_to_write_kvl, check_chat, extract_equations_regex
from bifura.kvl.compare import check_equation
from bifura.kvl.solver import COUPLED_INDUCTORS, Circuit, pretty
from bifura.llm.base import LLMError

C = Circuit(COUPLED_INDUCTORS)
CORRECT_1 = "-v1 + R1*i1 + L1*d(i1)/dt - M*d(i1 - i2)/dt + L2*d(i1 - i2)/dt - M*d(i1)/dt = 0"
CORRECT_2 = "-L2*d(i1 - i2)/dt + M*d(i1)/dt + R2*i2 = 0"


def test_derived_equations_match_the_dot_convention():
    eq1, eq2 = C.equations()
    assert pretty(eq1.expr, C) == "(L1 + L2 - 2·M)·di1/dt − (L2 - M)·di2/dt + R1·i1 − v1 = 0"
    assert pretty(eq2.expr, C) == "−(L2 - M)·di1/dt + L2·di2/dt + R2·i2 = 0"
    assert check_equation(CORRECT_1, C).ok and check_equation(CORRECT_1, C).mesh == "i1"
    assert check_equation(CORRECT_2, C).ok and check_equation(CORRECT_2, C).mesh == "i2"


def test_moving_a_dot_flips_the_mutual_signs():
    data = copy.deepcopy(COUPLED_INDUCTORS)
    next(e for e in data["elements"] if e["name"] == "L2")["dot"] = "top"
    c = Circuit(data)
    assert not check_equation(CORRECT_1, c).ok
    assert check_equation("-v1 + R1*i1 + L1*d(i1)/dt + M*d(i1 - i2)/dt + L2*d(i1 - i2)/dt + M*d(i1)/dt = 0", c).ok


@pytest.mark.parametrize("text", [
    "-v1(t) + R1i1(t) + L1(di1/dt) - Md(i1 - i2)/dt + L2d(i1 - i2)/dt - M*(di1/dt) = 0",   # student style
    "−v1(t)+R1i1(t)+L1dtdi1−Mdtd(i1−i2)+L2dtd(i1−i2)−Mdtdi1=0",                             # copy-paste garble
    r"-v_1 + R_1 i_1 + L_1 \frac{d i_1}{dt} - M \frac{d(i_1 - i_2)}{dt} + L_2 \frac{d(i_1-i_2)}{dt} - M\frac{di_1}{dt} = 0",
    "v1 - R1*i1 - L1*di1/dt + M*d(i1-i2)/dt - L2*d(i1-i2)/dt + M*di1/dt = 0",              # all signs flipped
    "(L1 + L2 - 2M) di1/dt - (L2 - M) di2/dt + R1 i1 = v1",                                 # grouped, v1 moved over
])
def test_many_ways_of_writing_the_correct_loop_1_equation(text):
    r = check_equation(text, C)
    assert r.parse_error is None and r.ok and r.mesh == "i1"


def test_geminis_wrong_equation_is_explained_term_by_term():
    r = check_equation("−v1(t)+R1i1(t)+(L1+2M+L2)dtdi1−(L2+M)dtdi2=0", C)
    assert not r.ok and r.mesh == "i1"
    assert {d.variable for d in r.diffs} == {"di1/dt", "di2/dt"}
    d = next(d for d in r.diffs if d.variable == "di1/dt")
    assert "2·M" in d.written and "- 2·M" in d.correct and any("dotted end" in x for x in d.contributions)


def test_unreadable_equation_is_reported():
    r = check_equation("-v1 + X9*i1 = 0", C)
    assert not r.ok and r.parse_error


def test_regex_fallback_finds_equations_without_an_ai():
    chat = "Gemini: loop 1 is −v1+R1i1+L1 di1/dt=0\nStudent: ok\n"
    found = extract_equations_regex(chat)
    assert len(found) == 1 and "R1i1" in found[0].equation


class FakeLLM:
    model = "fake"

    def __init__(self, replies):
        self.replies, self.seen = list(replies), []

    def next_json(self, system, turns):
        self.seen.append(turns[-1])
        if not self.replies:
            raise LLMError("busy")
        return self.replies.pop(0)


def test_chat_check_with_extracted_equations():
    llm = FakeLLM([{"equations": [
        {"turn": 2, "speaker": "assistant", "loop": "i1", "equation": "−v1+R1i1+L1 di1/dt+M di2/dt=0", "context": "loop 1"},
        {"turn": 3, "speaker": "student", "loop": "i1", "equation": CORRECT_1, "context": "my version"}]}])
    found, how = check_chat("(chat)", C, llm)
    assert [f.check.ok for f in found] == [False, True] and "AI" in how


def test_ai_is_corrected_without_being_given_the_answer():
    wrong = {"equations": [{"loop": "i1", "equation": CORRECT_1.replace("- M*d(i1)/dt", "+ M*d(i1)/dt")},
                           {"loop": "i2", "equation": CORRECT_2}]}
    right = {"equations": [{"loop": "i1", "equation": CORRECT_1}, {"loop": "i2", "equation": CORRECT_2}]}
    llm = FakeLLM([wrong, right])
    run = ask_ai_to_write_kvl(C, llm, image=(b"png", "image/png"))
    assert run.verified and len(run.attempts) == 2
    feedback = llm.seen[1]["text"]
    assert "Loop i1" in feedback and "di1/dt" in feedback and "2·M" not in feedback  # names the term, not the fix
    assert llm.seen[0]["image"] == (b"png", "image/png")


def test_missing_loop_is_not_verified():
    run = ask_ai_to_write_kvl(C, FakeLLM([{"equations": [{"loop": "i1", "equation": CORRECT_1}]}] * 3))
    assert not run.verified


def test_editable_table_round_trip():
    rows = _rows(COUPLED_INDUCTORS)
    data = _from_rows(rows, "i1, i2", "L1-L2: M")
    assert [str(e.expr) for e in Circuit(data).equations()] == [str(e.expr) for e in C.equations()]
