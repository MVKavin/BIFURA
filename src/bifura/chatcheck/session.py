"""Ask an AI a question, check its steps, ask it to correct itself, check again."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from bifura.chatcheck.checker import CheckReport, check_solution
from bifura.llm.base import LLMClient, LLMError

MAX_CORRECTIONS = 2

SOLVER_SYSTEM = """You are a friendly tutor for engineering students. Solve the user's problem step by step.
Reply with ONE JSON object in exactly this shape:
{"answer_text": "<the explanation you would normally give a student, 2-6 sentences>",
 "givens": {"<name>": <number>, ...},
 "steps": [{"explanation": "<what this step does>", "name": "<new quantity>", "formula": "<expression>",
            "value": <number>, "unit": "<unit>"}],
 "final": {"name": "<the quantity that answers the question>", "value": <number>, "unit": "<unit>"}}
Rules:
- givens: the numbers from the question, in base SI units (ohm, volt, ampere, second, ...).
- Each step computes ONE new quantity. Names are simple identifiers like R_total, I, V1, P_R1.
- formula uses only numbers, given/earlier names, + - * / ** ( ) and sqrt sin cos tan exp log pi.
  Write multiplication with *. Do not put "=" or units inside formula.
- value is the plain number your formula gives."""

DEMO_SLIP = ("\nDEMONSTRATION MODE: in one middle step, deliberately write a wrong value (a realistic "
             "arithmetic slip such as a wrong product or a dropped digit), keep its formula unchanged, and carry "
             "the wrong value into the later steps. Do not mention the slip anywhere.")

EXAMPLES = {
    "Series circuit (current and power)":
        "A 12 V battery is connected to two resistors in series, R1 = 4 ohm and R2 = 2 ohm. "
        "Find the current, the voltage across R1, and the power dissipated in R1.",
    "Voltage divider with a load":
        "A 24 V source feeds R1 = 10 kilo-ohm in series with R2 = 15 kilo-ohm. A 30 kilo-ohm load is connected "
        "across R2. Find the voltage across the load.",
    "Two-loop circuit with KVL":
        "Loop 1 has a 10 V source, R1 = 2 ohm and a shared resistor R3 = 4 ohm. Loop 2 has R2 = 3 ohm, "
        "the shared R3, and a 5 V source opposing the loop current. Using mesh analysis (KVL), find both mesh "
        "currents I1 and I2 (clockwise) and the current through R3.",
}


@dataclass
class Attempt:
    solution: dict[str, Any]
    report: CheckReport
    prompt_kind: str  # "question" or "correction"


@dataclass
class ChatRun:
    run_id: str
    question: str
    provider: str
    model: str
    demo_slip: bool
    expected: str | None
    attempts: list[Attempt] = field(default_factory=list)
    turns: list[dict[str, str]] = field(default_factory=list)
    error: str | None = None

    @property
    def first(self) -> Attempt | None:
        return self.attempts[0] if self.attempts else None

    @property
    def last(self) -> Attempt | None:
        return self.attempts[-1] if self.attempts else None

    @property
    def verified(self) -> bool:
        return bool(self.last and self.last.report.ok)

    @property
    def needed_fix(self) -> bool:
        return bool(self.first and not self.first.report.ok)


def correction_message(report: CheckReport) -> str:
    """Tell the AI exactly what Bifura's recalculation found (facts only, no hints about the fix)."""
    lines = ["Bifura recalculated every step of your solution with an exact calculator and found problems:"]
    lines += [f"- {p}" for p in report.given_problems]
    w = report.first_wrong
    if w:
        lines.append(f"- Step {w.n} ({w.name}): your formula {w.formula} gives {w.recomputed:.6g}, but you wrote {w.claimed:g}.")
    if report.affected:
        lines.append("- These later steps used that wrong number: " + ", ".join(f"{s.n} ({s.name})" for s in report.affected) + ".")
    for s in report.steps:
        if s.status == "unverifiable":
            lines.append(f"- Step {s.n} ({s.name}) could not be checked: {s.note}")
    if report.final_matches_expected is False:
        lines.append(f"- Your final answer {report.final_claimed:g} does not match the expected answer {report.expected_final:g}.")
    lines.append("Redo the whole solution correctly, in the same JSON format.")
    return "\n".join(lines)


def new_chat_id() -> str:
    return "C-" + datetime.now().strftime("%m%d-%H%M%S")


def run_chat_check(question: str, llm: LLMClient, provider: str, demo_slip: bool = False,
                   expected: str | None = None, progress: Callable[[str], None] = lambda m: None) -> ChatRun:
    run = ChatRun(new_chat_id(), question.strip(), provider, getattr(llm, "model", "?"), demo_slip, expected or None)
    run.turns.append({"role": "user", "text": run.question})
    system = SOLVER_SYSTEM + (DEMO_SLIP if demo_slip else "")
    for round_no in range(MAX_CORRECTIONS + 1):
        kind = "question" if round_no == 0 else "correction"
        progress(f"Asking {provider} ({run.model})…" if round_no == 0 else f"Asking {provider} to correct itself (round {round_no})…")
        try:
            # corrections never carry the demo instruction: the AI is asked to get it right
            solution = llm.next_json(system if round_no == 0 else SOLVER_SYSTEM, run.turns)
        except LLMError as exc:
            run.error = str(exc)
            progress(f"The AI could not answer: {exc}")
            break
        run.model = getattr(llm, "model", run.model)
        run.turns.append({"role": "model", "text": json.dumps(solution, ensure_ascii=False)})
        report = check_solution(run.question, solution, expected)
        run.attempts.append(Attempt(solution, report, kind))
        n_bad = sum(s.status in ("wrong", "affected") for s in report.steps)
        progress(f"Bifura recalculated {len(report.steps)} steps: "
                 + ("all correct ✓" if report.ok else f"first wrong step {report.first_wrong.n if report.first_wrong else '—'}, "
                    f"{n_bad} step(s) wrong or affected ✗"))
        if report.ok:
            break
        run.turns.append({"role": "user", "text": correction_message(report)})
    return run
