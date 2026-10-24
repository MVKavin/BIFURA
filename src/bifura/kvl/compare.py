"""Read a written KVL equation and compare it with the correct one, term by term."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache

import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

from bifura.kvl.solver import D, Circuit, MeshEquation, pretty

_TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)


def _split_identifier(tok: str, known: tuple[str, ...]) -> list[str] | None:
    """Split 'R1i1' into ['R1', 'i1'] using the circuit's known names (longest names first)."""
    @lru_cache(maxsize=None)
    def go(i: int) -> tuple[str, ...] | None:
        if i == len(tok):
            return ()
        for name in known:
            if tok.startswith(name, i):
                rest = go(i + len(name))
                if rest is not None:
                    return (name,) + rest
        return None
    out = go(0)
    return list(out) if out else None


def normalise(text: str, circuit: Circuit) -> str:
    """Turn the many ways people write derivatives into D(...) and split glued names."""
    s = str(text)
    s = s.replace("−", "-").replace("–", "-").replace("·", "*").replace("×", "*").replace("⋅", "*")
    s = re.sub(r"\\frac\{d\s*\(?([^{}]*?)\)?\}\{dt\}", r"D(\1)", s)       # LaTeX \frac{d i1}{dt}
    s = s.replace("\\left", "").replace("\\right", "").replace("$", "").replace("\\", "")
    s = re.sub(r"([A-Za-z])_\{?(\d+)\}?", r"\1\2", s)                       # LaTeX v_1 / v_{1} -> v1
    s = re.sub(r"\(\s*t\s*\)", "", s)                                        # i1(t), v1(t) -> i1, v1
    s = s.replace("{", "(").replace("}", ")")
    s = re.sub(r"\(\s*d\s*/\s*dt\s*\)\s*\(([^()]*)\)", r"D(\1)", s)          # (d/dt)(i1-i2)
    s = re.sub(r"\bd\s*/\s*dt\s*\(([^()]*)\)", r"D(\1)", s)                  # d/dt(i1)
    s = re.sub(r"(?<=[A-Za-z0-9_])d\s*\(([^()]*)\)\s*/\s*dt", r"*D(\1)", s)  # Md(i1-i2)/dt
    s = re.sub(r"\bd\s*\(([^()]*)\)\s*/\s*dt", r"D(\1)", s)                  # d(i1-i2)/dt
    s = re.sub(r"dtd\(([^()]*)\)", r"D(\1)", s)                              # pasted 'dtd(i1-i2)'
    meshes = "|".join(sorted(circuit.meshes, key=len, reverse=True))
    s = re.sub(rf"\bd\s*({meshes})\s*/\s*dt", r"D(\1)", s)                   # di1/dt
    s = re.sub(rf"dtd({meshes})", r"D(\1)", s)                               # pasted 'dtdi1'
    s = re.sub(rf"(?<=[A-Za-z0-9_])d({meshes})\s*/\s*dt", r"*D(\1)", s)      # L1di1/dt
    s = re.sub(rf"\bd({meshes})\b", r"D(\1)", s)                             # bare di1
    known = tuple(sorted(circuit.known_names(), key=len, reverse=True))
    def fix(m: re.Match) -> str:
        tok = m.group(0)
        if tok in known or tok == "D":
            return tok
        parts = _split_identifier(tok, known)
        return "*".join(parts) if parts else tok
    s = re.sub(r"[A-Za-z_][A-Za-z0-9_]*", fix, s)
    s = re.sub(r"(?<=[A-Za-z0-9_)])D\(", "*D(", s).replace("**D(", "*D(")
    names = "|".join(re.escape(n) for n in known)
    s = re.sub(rf"\b({names})\s*\(", r"\1*(", s)                             # L1(di1/dt) is a product, not a call
    return s


def parse_equation(text: str, circuit: Circuit) -> sp.Expr:
    """Equation text -> expression that must equal 0, with d/dt as D_<mesh> symbols."""
    s = normalise(text, circuit)
    if s.count("=") > 1:
        raise ValueError("more than one '=' in the equation")
    lhs, rhs = (s.split("=") + ["0"])[:2] if "=" in s else (s, "0")
    Dfun = sp.Function("D")
    local = {n: sp.Symbol(n) for n in circuit.known_names()}
    local["D"] = Dfun
    expr = parse_expr(lhs, local_dict=local, transformations=_TRANSFORMS) - \
        parse_expr(rhs or "0", local_dict=local, transformations=_TRANSFORMS)

    def lin(arg: sp.Expr) -> sp.Expr:                     # D is linear: D(i1 - i2) = D_i1 - D_i2
        arg = sp.expand(arg)
        out = sp.Integer(0)
        for m in circuit.meshes:
            out += arg.coeff(sp.Symbol(m)) * D(m)
        return out
    expr = expr.replace(lambda e: isinstance(e, sp.Function) and e.func == Dfun, lambda e: lin(e.args[0]))
    unknown = sorted(str(x) for x in expr.free_symbols
                     if str(x) not in circuit.known_names() and not str(x).startswith("D_"))
    if unknown:
        raise ValueError("unknown names: " + ", ".join(unknown))
    return sp.expand(expr)


@dataclass
class TermDiff:
    variable: str          # e.g. 'di2/dt'
    written: str
    correct: str
    contributions: list[str] = field(default_factory=list)   # reasons from the correct derivation


@dataclass
class EquationCheck:
    text: str
    mesh: str | None
    ok: bool
    parse_error: str | None = None
    diffs: list[TermDiff] = field(default_factory=list)
    flipped: bool = False      # equation was written with all signs flipped (still correct)
    written_pretty: str = ""
    correct_pretty: str = ""


def _label(v: sp.Symbol) -> str:
    n = str(v)
    return f"d{n[2:]}/dt" if n.startswith("D_") else n


def _fmt(c: sp.Expr) -> str:
    c = sp.simplify(c)
    return "0 (missing)" if c == 0 else str(c).replace("*", "·")


def compare(written: sp.Expr, eq: MeshEquation, circuit: Circuit) -> tuple[list[TermDiff], bool]:
    correct = eq.expr
    best = None
    for k in (1, -1):
        diffs = []
        for v in circuit.variables():
            cw, cc = sp.expand(k * written).coeff(v), correct.coeff(v)
            if sp.simplify(cw - cc) != 0:
                reasons = [t.reason for t in eq.terms if sp.expand(t.expr).coeff(v) != 0]
                diffs.append(TermDiff(_label(v), _fmt(cw), _fmt(cc), reasons))
        rest = sp.simplify(sp.expand(k * written) - sum(sp.expand(k * written).coeff(v) * v for v in circuit.variables())
                           - (correct - sum(correct.coeff(v) * v for v in circuit.variables())))
        if rest != 0:
            diffs.append(TermDiff("other terms", _fmt(rest), "0"))
        if best is None or len(diffs) < len(best[0]):
            best = (diffs, k == -1)
    return best


def check_equation(text: str, circuit: Circuit, mesh: str | None = None) -> EquationCheck:
    """Check one written equation. If ``mesh`` is not given, use the loop it matches best."""
    try:
        written = parse_equation(text, circuit)
    except Exception as exc:
        return EquationCheck(text, mesh, False, parse_error=f"Could not read this equation ({exc}).")
    eqs = {e.mesh: e for e in circuit.equations()}
    candidates = [mesh] if mesh in eqs else list(eqs)
    results = []
    for m in candidates:
        diffs, flipped = compare(written, eqs[m], circuit)
        results.append((len(diffs), m, diffs, flipped))
    n, m, diffs, flipped = min(results, key=lambda r: r[0])
    return EquationCheck(text, m, n == 0, None, diffs, flipped, pretty(written, circuit), pretty(eqs[m].expr, circuit))
