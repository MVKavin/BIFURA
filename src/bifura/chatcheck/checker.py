"""Recalculate an AI's step-by-step solution with SymPy.

Each step is ``{"name": "R_total", "formula": "R1 + R2", "value": 6}``. A step is
*wrong* when its formula, evaluated with the AI's own earlier values, does not give
the value it claims. A later step is *affected* when its arithmetic is fine but it
inherited a wrong number (its value differs from the fully recalculated "true" chain).
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Any

import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

REL_TOL = 0.005   # 0.5 %: allows normal rounding by the AI
ABS_TOL = 1e-6
_FUNCS = {"sqrt": sp.sqrt, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "exp": sp.exp, "log": sp.log,
          "ln": sp.log, "abs": sp.Abs, "asin": sp.asin, "acos": sp.acos, "atan": sp.atan, "pi": sp.pi}
_TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)
_IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _num(value: Any) -> float | None:
    """Pull a number out of 6, "6", "6.0 ohm", "-88.2 %", "2e-3"."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    m = re.search(r"[-+]?\d[\d,]*\.?\d*(?:[eE][-+]?\d+)?", str(value or ""))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def close(a: float, b: float) -> bool:
    return abs(a - b) <= max(ABS_TOL, REL_TOL * max(abs(a), abs(b)))


def parse(formula: str) -> sp.Expr:
    """Parse a formula; every identifier that is not a known function becomes a plain symbol
    (so names like I, E, S, Q are quantities, not SymPy's imaginary unit etc.)."""
    text = str(formula).replace("×", "*").replace("·", "*").replace("−", "-").replace("÷", "/")
    local = {name: _FUNCS.get(name, sp.Symbol(name)) for name in _IDENT.findall(text)}
    return parse_expr(text, local_dict=local, transformations=_TRANSFORMS, evaluate=True)


def _evaluate(expr: sp.Expr, values: dict[str, float]) -> tuple[float | None, list[str]]:
    missing = sorted(str(s) for s in expr.free_symbols if str(s) not in values)
    if missing:
        return None, missing
    out = complex(expr.subs({sp.Symbol(k): v for k, v in values.items()}).evalf())
    if abs(out.imag) > 1e-9 or math.isnan(out.real):
        return None, []
    return float(out.real), []


@dataclass
class StepCheck:
    n: int
    name: str
    formula: str
    claimed: float | None
    explanation: str = ""
    uses: list[str] = field(default_factory=list)
    recomputed: float | None = None       # formula with the AI's own earlier values
    true_value: float | None = None       # formula with fully corrected earlier values
    status: str = "ok"                    # ok | wrong | affected | unverifiable
    note: str = ""
    mistake_type: str | None = None


@dataclass
class CheckReport:
    givens: dict[str, float]
    given_problems: list[str]
    steps: list[StepCheck]
    final_name: str | None
    final_claimed: float | None
    final_true: float | None
    expected_final: float | None = None

    @property
    def first_wrong(self) -> StepCheck | None:
        return next((s for s in self.steps if s.status == "wrong"), None)

    @property
    def affected(self) -> list[StepCheck]:
        return [s for s in self.steps if s.status == "affected"]

    @property
    def final_matches_expected(self) -> bool | None:
        if self.expected_final is None or self.final_claimed is None:
            return None
        return close(self.final_claimed, self.expected_final)

    @property
    def ok(self) -> bool:
        return (not self.given_problems and self.first_wrong is None and not self.affected
                and self.final_matches_expected is not False
                and all(s.status != "unverifiable" for s in self.steps))


def classify_slip(formula: str, values: dict[str, float], claimed: float, correct: float) -> str:
    """Rule-based guess at the kind of slip (a hypothesis, labelled as such in the UI)."""
    if correct != 0 and claimed != 0:
        ratio = claimed / correct
        if close(ratio, -1):
            return "sign error"
        for k in range(1, 7):
            if close(ratio, 10 ** k) or close(ratio, 10 ** -k):
                return "decimal / unit slip (off by a power of 10)"
        if close(claimed * correct, 1):
            return "upside-down division"
    swaps = [("+", "-"), ("-", "+"), ("*", "/"), ("/", "*")]
    for a, b in swaps:
        for i, ch in enumerate(formula):
            if ch == a:
                alt = formula[:i] + b + formula[i + 1:]
                try:
                    v, missing = _evaluate(parse(alt), values)
                except Exception:
                    continue
                if v is not None and not missing and close(v, claimed):
                    return f"used '{b}' instead of '{a}'"
    return "arithmetic slip"


def check_solution(question: str, solution: dict[str, Any], expected_final: Any = None) -> CheckReport:
    givens_raw = solution.get("givens") or {}
    givens = {str(k): _num(v) for k, v in givens_raw.items()}
    given_problems = []
    q_numbers = [_num(m) for m in re.findall(r"[-+]?\d[\d,]*\.?\d*(?:[eE][-+]?\d+)?", question or "")]
    q_numbers = [x for x in q_numbers if x is not None]
    for k, v in givens.items():
        if v is None:
            given_problems.append(f"Given '{k}' has no number.")
        elif q_numbers and not any(close(v, x) or close(abs(v), abs(x)) for x in q_numbers):
            given_problems.append(f"Given {k} = {v:g} does not appear in the question.")
    givens = {k: v for k, v in givens.items() if v is not None}

    ai_values = dict(givens)    # what the AI believed at each point
    true_values = dict(givens)  # fully recalculated chain
    steps: list[StepCheck] = []
    for i, raw in enumerate(solution.get("steps") or [], 1):
        name = str(raw.get("name") or f"step{i}").strip()
        formula = str(raw.get("formula") or "").strip()
        claimed = _num(raw.get("value"))
        st = StepCheck(n=i, name=name, formula=formula, claimed=claimed, explanation=str(raw.get("explanation") or ""))
        try:
            expr = parse(formula)
            st.uses = sorted(str(s) for s in expr.free_symbols)
            st.recomputed, missing = _evaluate(expr, ai_values)
            st.true_value, _ = _evaluate(expr, true_values)
        except Exception as exc:
            st.status, st.note = "unverifiable", f"Could not read the formula ({type(exc).__name__})."
            steps.append(st)
            if claimed is not None:
                ai_values[name] = true_values[name] = claimed
            continue
        if missing:
            st.status, st.note = "unverifiable", "Uses quantities that were never defined: " + ", ".join(missing)
        elif claimed is None or st.recomputed is None:
            st.status, st.note = "unverifiable", "No numeric value to check."
        elif not close(claimed, st.recomputed):
            st.status = "wrong"
            st.note = f"{formula} = {st.recomputed:.6g}, not {claimed:g}"
            st.mistake_type = classify_slip(formula, ai_values, claimed, st.recomputed)
        elif st.true_value is not None and not close(claimed, st.true_value):
            st.status = "affected"
            st.note = f"Arithmetic is right, but it used a wrong earlier number (should be {st.true_value:.6g})."
        ai_values[name] = claimed if claimed is not None else (st.recomputed or 0.0)
        true_values[name] = st.true_value if st.true_value is not None else ai_values[name]
        steps.append(st)

    final = solution.get("final") or {}
    final_name = str(final.get("name") or (steps[-1].name if steps else "")) or None
    final_claimed = _num(final.get("value")) if final else (steps[-1].claimed if steps else None)
    final_true = true_values.get(final_name) if final_name else None
    return CheckReport(givens, given_problems, steps, final_name, final_claimed, final_true, _num(expected_final))
