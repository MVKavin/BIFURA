"""Derive mesh (KVL) equations from a simple circuit description.

Circuit description (JSON-friendly)::

    {"meshes": ["i1", "i2"],            # mesh currents, all drawn clockwise
     "elements": [
        {"name": "v1", "type": "V", "axis": "vertical", "plus": "top",  "currents": {"i1": "up"}},
        {"name": "R1", "type": "R", "axis": "horizontal",               "currents": {"i1": "right"}},
        {"name": "L1", "type": "L", "axis": "horizontal", "dot": "left", "currents": {"i1": "right"}},
        {"name": "L2", "type": "L", "axis": "vertical", "dot": "bottom", "currents": {"i1": "down", "i2": "up"}},
        {"name": "R2", "type": "R", "axis": "vertical",                 "currents": {"i2": "down"}}],
     "couplings": [{"a": "L1", "b": "L2", "M": "M"}]}

Rules used (standard textbook conventions):
- Walking a loop in its current's direction, a resistor or inductor gives a voltage *drop*.
- A source gives -V if the walk enters its - end and leaves at + (a rise), +V otherwise.
- Mutual term on inductor A from inductor B: +M d(i_B)/dt if the currents (taken in A's and B's
  reference directions) both enter their dotted ends or both leave them; otherwise -M d(i_B)/dt.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import sympy as sp

ENTRY = {"right": "left", "left": "right", "down": "top", "up": "bottom"}
EXIT = {"right": "right", "left": "left", "down": "bottom", "up": "top"}
OPPOSITE = {"right": "left", "left": "right", "up": "down", "down": "up"}


def D(name: str) -> sp.Symbol:
    """Symbol standing for d(name)/dt."""
    return sp.Symbol(f"D_{name}")


@dataclass
class Term:
    element: str
    expr: sp.Expr
    text: str          # e.g. "−M·d(i1 − i2)/dt"
    reason: str        # plain-English why


@dataclass
class MeshEquation:
    mesh: str
    terms: list[Term] = field(default_factory=list)

    @property
    def expr(self) -> sp.Expr:
        return sp.expand(sum((t.expr for t in self.terms), sp.Integer(0)))


def _cur_text(ref: dict[str, int]) -> str:
    parts = []
    for m, s in ref.items():
        parts.append(("− " if s < 0 else ("+ " if parts else "")) + m)
    txt = " ".join(parts).strip()
    return txt if len(ref) == 1 and list(ref.values())[0] > 0 else f"({txt})"


def _signed(coef: str, sign: int, body: str) -> str:
    return f"{'+' if sign > 0 else '−'}{coef}{body}"


class Circuit:
    def __init__(self, data: dict[str, Any]):
        self.data = data
        self.meshes: list[str] = list(data["meshes"])
        self.elements = {e["name"]: e for e in data["elements"]}
        self.couplings = list(data.get("couplings") or [])
        self.symbols = {n: sp.Symbol(n) for n in list(self.elements) + self.meshes
                        + [c.get("M", "M") for c in self.couplings]}
        for e in self.elements.values():
            if e["type"] not in ("R", "L", "V"):
                raise ValueError(f"{e['name']}: only R, L and V elements are supported (got {e['type']}).")
            for m, d in e["currents"].items():
                if m not in self.meshes or d not in ENTRY:
                    raise ValueError(f"{e['name']}: bad current entry {m}: {d}")

    # reference direction of an element = direction of its first listed mesh current
    def ref_dir(self, name: str) -> str:
        return next(iter(self.elements[name]["currents"].values()))

    def branch_current(self, name: str) -> dict[str, int]:
        ref = self.ref_dir(name)
        return {m: (1 if d == ref else -1) for m, d in self.elements[name]["currents"].items()}

    def _current_expr(self, coeffs: dict[str, int]) -> sp.Expr:
        return sum((s * sp.Symbol(m) for m, s in coeffs.items()), sp.Integer(0))

    def _d_expr(self, coeffs: dict[str, int]) -> sp.Expr:
        return sum((s * D(m) for m, s in coeffs.items()), sp.Integer(0))

    def enters_dot(self, name: str) -> bool:
        e = self.elements[name]
        return ENTRY[self.ref_dir(name)] == e.get("dot")

    def mesh_equation(self, mesh: str) -> MeshEquation:
        eq = MeshEquation(mesh)
        for name, e in self.elements.items():
            if mesh not in e["currents"]:
                continue
            walk = e["currents"][mesh]
            ref = self.ref_dir(name)
            k = 1 if walk == ref else -1          # walking with (+) or against (-) the element's reference
            I = self.branch_current(name)
            Itxt = _cur_text(I)
            sym = self.symbols[name]
            if e["type"] == "V":
                rise = EXIT[walk] == e.get("plus")
                eq.terms.append(Term(name, (-sym if rise else sym),
                                     f"{'−' if rise else '+'}{name}",
                                     f"Walking {walk} through {name}, we go from its {'−' if rise else '+'} end to its "
                                     f"{'+' if rise else '−'} end: a voltage {'rise' if rise else 'drop'}, so "
                                     f"{'−' if rise else '+'}{name}."))
                continue
            if e["type"] == "R":
                eq.terms.append(Term(name, k * sym * self._current_expr(I), _signed(name, k, f"·{Itxt}"),
                                     f"{name} carries {Itxt} ({ref}). We walk {'with' if k > 0 else 'against'} it, "
                                     f"so Ohm's law gives {'+' if k > 0 else '−'}{name}·{Itxt}."))
                continue
            # inductor: self term
            eq.terms.append(Term(name, k * sym * self._d_expr(I), _signed(name, k, f"·d{Itxt}/dt"),
                                 f"{name} carries {Itxt} ({ref}). Self-induced voltage {name}·d{Itxt}/dt, "
                                 f"{'+' if k > 0 else '−'} because we walk {'with' if k > 0 else 'against'} that current."))
            # mutual terms
            for c in self.couplings:
                if name not in (c["a"], c["b"]):
                    continue
                other = c["b"] if c["a"] == name else c["a"]
                Mname = c.get("M", "M")
                Io = self.branch_current(other)
                Iotxt = _cur_text(Io)
                same = self.enters_dot(name) == self.enters_dot(other)
                s = (1 if same else -1) * k
                here = "enters" if self.enters_dot(name) else "leaves"
                there = "enters" if self.enters_dot(other) else "leaves"
                eq.terms.append(Term(name, s * self.symbols[Mname] * self._d_expr(Io), _signed(Mname, s, f"·d{Iotxt}/dt"),
                                     f"Mutual voltage on {name} comes from the current in {other}, which is {Iotxt}. "
                                     f"{Itxt} {here} {name}'s dotted end and {Iotxt} {there} {other}'s dotted end: "
                                     f"{'both the same, so +' if same else 'opposite, so −'}M"
                                     + ("" if k > 0 else ", then flipped because we walk against " + name + "'s current")
                                     + f" → {'+' if s > 0 else '−'}{Mname}·d{Iotxt}/dt."))
        return eq

    def equations(self) -> list[MeshEquation]:
        return [self.mesh_equation(m) for m in self.meshes]

    def variables(self) -> list[sp.Symbol]:
        srcs = [self.symbols[n] for n, e in self.elements.items() if e["type"] == "V"]
        return [D(m) for m in self.meshes] + [sp.Symbol(m) for m in self.meshes] + srcs

    def known_names(self) -> list[str]:
        return list(self.symbols)


def pretty(expr: sp.Expr, circuit: Circuit) -> str:
    """Readable text form, grouped by d/dt and current terms: e.g. '(L1 + L2 − 2M)·di1/dt + …'."""
    expr = sp.expand(expr)
    out = []
    for v in circuit.variables():
        c = sp.simplify(expr.coeff(v))
        if c == 0:
            continue
        name = str(v)
        label = f"d{name[2:]}/dt" if name.startswith("D_") else name
        cs = str(c).replace("*", "·")
        if c == 1:
            out.append(f"+ {label}")
        elif c == -1:
            out.append(f"− {label}")
        elif c.could_extract_minus_sign():
            ncs = str(-c).replace("*", "·")
            out.append(f"− ({ncs})·{label}" if " " in ncs else f"− {ncs}·{label}")
        else:
            out.append(f"+ ({cs})·{label}" if " " in cs else f"+ {cs}·{label}")
    s = " ".join(out).strip()
    return (s[2:] if s.startswith("+ ") else s.replace("− ", "−", 1)) + " = 0"


def latex(expr: sp.Expr, circuit: Circuit) -> str:
    names = {D(m): r"\frac{d" + sp.latex(sp.Symbol(m)) + r"}{dt}" for m in circuit.meshes}
    grouped = sp.collect(sp.expand(expr), circuit.variables())
    return sp.latex(grouped, symbol_names=names) + " = 0"


COUPLED_INDUCTORS = {
    "name": "Coupled inductors (L1, L2 with mutual inductance M)",
    "image": "coupled_inductors.png",
    "meshes": ["i1", "i2"],
    "elements": [
        {"name": "v1", "type": "V", "axis": "vertical", "plus": "top", "currents": {"i1": "up"}},
        {"name": "R1", "type": "R", "axis": "horizontal", "currents": {"i1": "right"}},
        {"name": "L1", "type": "L", "axis": "horizontal", "dot": "left", "currents": {"i1": "right"}},
        {"name": "L2", "type": "L", "axis": "vertical", "dot": "bottom", "currents": {"i1": "down", "i2": "up"}},
        {"name": "R2", "type": "R", "axis": "vertical", "currents": {"i2": "down"}},
    ],
    "couplings": [{"a": "L1", "b": "L2", "M": "M"}],
}
