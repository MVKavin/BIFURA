"""The AI-facing parts of KVL check: read a circuit picture, pull equations out of a chat,
and ask an AI to write KVL (then correct it). Bifura's own solver decides what is right."""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from bifura.kvl.compare import EquationCheck, check_equation
from bifura.kvl.solver import Circuit
from bifura.llm.base import LLMClient, LLMError

MAX_CORRECTIONS = 2

READ_CIRCUIT_SYSTEM = """You read circuit diagrams for a mesh-analysis (KVL) checker. Describe the circuit as JSON:
{"meshes": ["i1", "i2"],
 "elements": [{"name": "R1", "type": "R"|"L"|"V", "axis": "horizontal"|"vertical",
               "plus": "top"|"bottom"|"left"|"right" (V only: the + end),
               "dot": "top"|"bottom"|"left"|"right" (L only, if it has a dot; else omit),
               "currents": {"i1": "up"|"down"|"left"|"right", ...}}],
 "couplings": [{"a": "L1", "b": "L2", "M": "M"}]}
Rules:
- Mesh currents are clockwise, named as in the picture (i1 = left loop, i2 = next, ...).
- "currents" lists every mesh current that flows through that element and its direction there
  (a clockwise loop goes up its left side, right along its top, down its right side, left along its bottom).
  A branch shared by two loops lists both currents (they flow in opposite directions there).
- Use the element names printed in the picture. Look very carefully at which END each dot is on.
- Wires are not elements."""

EXTRACT_SYSTEM = """You extract equations from a tutoring chat about circuits. Do NOT correct anything.
Return JSON: {"equations": [{"turn": <1-based message number>, "speaker": "assistant"|"student",
  "loop": "i1"|"i2"|null, "equation": "<the equation exactly as written, same signs and terms>",
  "context": "<5-12 words: what this equation was presented as>"}]}
- Include every KVL / mesh equation that is a complete equation (has '=').
- Keep the order they appear. If the same equation is repeated in a regrouped form, include it again.
- You may rewrite derivative notation only (e.g. "L1dtdi1" -> "L1*d(i1)/dt"); never change signs or terms."""

WRITE_KVL_SYSTEM = """You are a tutor. Write the mesh (KVL) equations for the circuit. Do not solve them.
Reply with JSON: {"explanation": "<short explanation for a first-year student>",
 "equations": [{"loop": "<mesh current name>", "equation": "<... = 0>"}]}
Write derivatives as d(x)/dt, e.g. L1*d(i1)/dt - M*d(i1 - i2)/dt. Use the names from the circuit."""


def describe(circuit: Circuit) -> str:
    """Plain-text description of the circuit data (sent along with the picture)."""
    lines = [f"Mesh currents (clockwise): {', '.join(circuit.meshes)}."]
    for n, e in circuit.elements.items():
        bits = [f"{n}: {dict(R='resistor', L='inductor', V='voltage source')[e['type']]}"]
        if e.get("plus"):
            bits.append(f"+ terminal at the {e['plus']}")
        if e.get("dot"):
            bits.append(f"dot at the {e['dot']} end")
        bits.append("currents: " + ", ".join(f"{m} flows {d}" for m, d in e["currents"].items()))
        lines.append("; ".join(bits))
    for c in circuit.couplings:
        lines.append(f"{c['a']} and {c['b']} are magnetically coupled with mutual inductance {c.get('M', 'M')}.")
    return "\n".join(lines)


def read_circuit_image(image: bytes, mime: str, llm: LLMClient) -> dict[str, Any]:
    data = llm.next_json(READ_CIRCUIT_SYSTEM, [{"role": "user", "text": "Describe this circuit.", "image": (image, mime)}])
    Circuit(data)  # raises if the structure is unusable
    return data


@dataclass
class FoundEquation:
    turn: int | None
    speaker: str
    loop: str | None
    equation: str
    context: str
    check: EquationCheck | None = None


def extract_equations_regex(chat: str) -> list[FoundEquation]:
    """Offline fallback: any line fragment ending in '= 0' that mentions a current."""
    out = []
    for i, line in enumerate(chat.splitlines(), 1):
        for m in re.finditer(r"[^\n:]*?=\s*0\b", line):
            text = m.group(0).strip(" .*-•")
            if re.search(r"i\s*_?\{?\d", text):
                out.append(FoundEquation(None, "unknown", None, text, f"line {i}"))
    return out


def extract_equations(chat: str, llm: LLMClient | None) -> tuple[list[FoundEquation], str]:
    if llm is not None:
        try:
            data = llm.next_json(EXTRACT_SYSTEM, [{"role": "user", "text": chat[:30000]}])
            eqs = [FoundEquation(e.get("turn"), str(e.get("speaker") or "unknown"), e.get("loop"),
                                 str(e.get("equation") or ""), str(e.get("context") or ""))
                   for e in data.get("equations") or [] if e.get("equation")]
            if eqs:
                return eqs, "read by the AI (equations copied, not corrected)"
        except LLMError:
            pass
    return extract_equations_regex(chat), "found by pattern matching (no AI available)"


def check_chat(chat: str, circuit: Circuit, llm: LLMClient | None) -> tuple[list[FoundEquation], str]:
    found, how = extract_equations(chat, llm)
    for f in found:
        loop = f.loop if f.loop in circuit.meshes else None
        f.check = check_equation(f.equation, circuit, loop)
    return found, how


@dataclass
class KvlAttempt:
    reply: dict[str, Any]
    checks: list[EquationCheck]
    meshes: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """Every equation correct and every loop covered."""
        return bool(self.checks) and all(c.ok for c in self.checks) and {c.mesh for c in self.checks} >= set(self.meshes)


@dataclass
class KvlRun:
    attempts: list[KvlAttempt] = field(default_factory=list)
    error: str | None = None
    model: str = ""

    @property
    def verified(self) -> bool:
        return bool(self.attempts) and self.attempts[-1].ok


def _feedback(checks: list[EquationCheck], meshes: list[str]) -> str:
    """Tell the AI what is wrong without handing over the answer."""
    lines = ["Bifura derived the KVL equations independently and compared yours term by term:"]
    seen = set()
    for c in checks:
        seen.add(c.mesh)
        if c.parse_error:
            lines.append(f"- {c.text!r}: could not be read. Use the requested notation.")
        elif not c.ok:
            terms = ", ".join(d.variable for d in c.diffs)
            lines.append(f"- Loop {c.mesh}: the terms in {terms} are wrong. Re-check the dot convention and which "
                         "current flows through each coupled inductor.")
    for m in meshes:
        if m not in seen:
            lines.append(f"- Loop {m}: missing.")
    lines.append("Write all the equations again, corrected, in the same JSON format.")
    return "\n".join(lines)


def ask_ai_to_write_kvl(circuit: Circuit, llm: LLMClient, image: tuple[bytes, str] | None = None,
                        progress: Callable[[str], None] = lambda m: None) -> KvlRun:
    run = KvlRun(model=getattr(llm, "model", ""))
    first = {"role": "user", "text": "Write the mesh (KVL) equations for this circuit.\nCircuit data:\n" + describe(circuit)}
    if image:
        first["image"] = image
    turns = [first]
    for round_no in range(MAX_CORRECTIONS + 1):
        progress("Asking the AI to write the KVL equations…" if round_no == 0 else f"Asking the AI to correct them (round {round_no})…")
        try:
            reply = llm.next_json(WRITE_KVL_SYSTEM, turns)
        except LLMError as exc:
            run.error = str(exc)
            progress(f"The AI could not answer: {exc}")
            break
        run.model = getattr(llm, "model", run.model)
        checks = [check_equation(str(e.get("equation") or ""), circuit,
                                 e.get("loop") if e.get("loop") in circuit.meshes else None)
                  for e in reply.get("equations") or []]
        run.attempts.append(KvlAttempt(reply, checks, list(circuit.meshes)))
        bad = [c for c in checks if not c.ok]
        progress("Bifura checked the equations: " + ("all correct ✓" if checks and not bad else f"{len(bad)} wrong ✗"))
        if run.attempts[-1].ok:
            break
        turns.append({"role": "model", "text": json.dumps(reply, ensure_ascii=False)})
        turns.append({"role": "user", "text": _feedback(checks, circuit.meshes)})
    return run
