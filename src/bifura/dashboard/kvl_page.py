"""Streamlit "KVL circuit check" mode: check KVL equations from a chat, an AI, or a student."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import streamlit as st

from bifura.kvl.ai import ask_ai_to_write_kvl, check_chat, read_circuit_image
from bifura.kvl.compare import EquationCheck, check_equation
from bifura.kvl.solver import COUPLED_INDUCTORS, Circuit, latex
from bifura.llm import PROVIDERS, get_llm, provider_status

CIRCUITS = Path(__file__).resolve().parents[3] / "data" / "circuits"
DIRS = ["up", "down", "left", "right"]


def sidebar_settings() -> dict[str, Any]:
    st.markdown("#### AI used by the KVL check")
    statuses = {p: provider_status(p) for p in PROVIDERS}
    options = list(PROVIDERS)
    default = next((i for i, p in enumerate(options) if statuses[p].ready), 0)
    provider = st.radio("AI model", options, index=default, key="kvl_provider",
                        format_func=lambda p: PROVIDERS[p]["label"] + ("" if statuses[p].ready else "  (not set up)"))
    st.caption("The AI only reads pictures/chats and writes equations. "
               "Bifura's own solver decides what is correct.")
    return {"provider": provider, "ready": statuses[provider].ready}


# ---------- circuit data <-> editable table ----------------------------------------------------

def _rows(data: dict[str, Any]) -> list[dict[str, str]]:
    rows = []
    for e in data["elements"]:
        rows.append({"name": e["name"], "type": e["type"], "axis": e.get("axis", ""),
                     "+ end (sources)": e.get("plus", ""), "dot end (inductors)": e.get("dot", ""),
                     "loop currents through it": ", ".join(f"{m} {d}" for m, d in e["currents"].items())})
    return rows


def _from_rows(rows: list[dict[str, Any]], meshes: str, couplings: str) -> dict[str, Any]:
    elements = []
    for r in rows:
        if not str(r.get("name") or "").strip():
            continue
        cur = {}
        for part in str(r.get("loop currents through it") or "").split(","):
            bits = part.split()
            if len(bits) == 2 and bits[1] in DIRS:
                cur[bits[0]] = bits[1]
        e = {"name": str(r["name"]).strip(), "type": str(r["type"]).strip().upper(), "axis": r.get("axis") or "",
             "currents": cur}
        if str(r.get("+ end (sources)") or "").strip():
            e["plus"] = str(r["+ end (sources)"]).strip()
        if str(r.get("dot end (inductors)") or "").strip():
            e["dot"] = str(r["dot end (inductors)"]).strip()
        elements.append(e)
    cps = []
    for part in couplings.split(","):
        if "-" in part and ":" in part:
            pair, m = part.split(":")
            a, b = [x.strip() for x in pair.split("-")]
            cps.append({"a": a, "b": b, "M": m.strip()})
    return {"meshes": [m.strip() for m in meshes.split(",") if m.strip()], "elements": elements, "couplings": cps}


def circuit_section(settings: dict[str, Any]) -> tuple[Circuit | None, tuple[bytes, str] | None]:
    ss = st.session_state
    st.markdown("### 1 · The circuit")
    source = st.radio("Circuit", ["example", "upload"], horizontal=True, key="kvl_source",
                      format_func=lambda s: {"example": "Example: coupled inductors (your circuit)",
                                             "upload": "Upload my own circuit picture"}[s])
    image: tuple[bytes, str] | None = None
    if source == "example":
        img = CIRCUITS / COUPLED_INDUCTORS["image"]
        image = (img.read_bytes(), "image/png")
        if ss.get("kvl_loaded") != "example":
            ss.kvl_data, ss.kvl_loaded = copy.deepcopy(COUPLED_INDUCTORS), "example"
    else:
        up = st.file_uploader("Circuit picture (PNG or JPG)", type=["png", "jpg", "jpeg"], key="kvl_img")
        if up is None:
            st.info("Upload a picture of a circuit with clearly drawn loop currents (and dots for coupled inductors).")
            return None, None
        image = (up.getvalue(), up.type or "image/png")
        if ss.get("kvl_loaded") != up.name:
            ss.kvl_data, ss.kvl_loaded = None, up.name
        if ss.kvl_data is None:
            if not settings["ready"]:
                st.error(f"{PROVIDERS[settings['provider']]['label']} is not set up, so the picture cannot be read.")
                return None, image
            if st.button("Read the circuit with AI", type="primary"):
                with st.spinner("Reading the picture…"):
                    try:
                        ss.kvl_data = read_circuit_image(image[0], image[1], get_llm(settings["provider"]))
                    except Exception as exc:
                        st.error(f"Could not read the circuit: {exc}")
                        return None, image
                st.rerun()
    c1, c2 = st.columns([2, 3])
    c1.image(image[0], use_container_width=True)
    data = ss.kvl_data
    if data is None:
        return None, image
    with c2:
        st.caption("What Bifura uses (check it against the picture, especially **which end each dot is on**). "
                   "You can edit any cell.")
        rows = st.data_editor(_rows(data), num_rows="dynamic", use_container_width=True, key=f"kvl_table_{ss.kvl_loaded}",
                              column_config={"type": st.column_config.SelectboxColumn(options=["R", "L", "V"]),
                                             "axis": st.column_config.SelectboxColumn(options=["horizontal", "vertical"])})
        a, b = st.columns(2)
        meshes = a.text_input("Loop currents (clockwise)", ", ".join(data["meshes"]), key=f"kvl_meshes_{ss.kvl_loaded}")
        couplings = b.text_input("Coupled inductors", ", ".join(f"{c['a']}-{c['b']}: {c.get('M', 'M')}" for c in data.get("couplings", [])),
                                 key=f"kvl_coupl_{ss.kvl_loaded}", help="Format: L1-L2: M")
    try:
        edited = _from_rows(rows if isinstance(rows, list) else rows.to_dict("records"), meshes, couplings)
        return Circuit(edited), image
    except Exception as exc:
        st.error(f"The circuit data is not complete yet: {exc}")
        return None, image


# ---------- rendering helpers -------------------------------------------------------------------

def show_check(c: EquationCheck, circuit: Circuit, key: str) -> None:
    if c.parse_error:
        st.warning(c.parse_error)
        return
    if c.ok:
        st.success(f"Correct KVL for loop {c.mesh}" + (" (written with all signs flipped, which is fine)." if c.flipped else "."), icon=":material/check_circle:")
        return
    st.error(f"Wrong KVL for loop {c.mesh}: {len(c.diffs)} term(s) do not match.", icon=":material/cancel:")
    st.dataframe([{"Term": d.variable, "Written": d.written, "Correct": d.correct} for d in c.diffs],
                 hide_index=True, use_container_width=True)
    with st.expander("Why? (how Bifura derives these terms)"):
        for d in c.diffs:
            st.markdown(f"**{d.variable}**")
            for r in d.contributions:
                st.markdown(f"- {r}")


def correct_section(circuit: Circuit) -> None:
    st.markdown("### 2 · Bifura's correct KVL")
    with st.expander("Show the correct equations, step by step (hidden so you can try first)", expanded=False):
        for eq in circuit.equations():
            st.markdown(f"**Loop {eq.mesh}** (walk clockwise, add the voltage drops):")
            st.latex(latex(eq.expr, circuit))
            st.markdown("  " + "  ".join(f"`{t.text}`" for t in eq.terms) + "  `= 0`")
            for t in eq.terms:
                st.markdown(f"- `{t.text}`: {t.reason}")


def chat_tab(circuit: Circuit, settings: dict[str, Any]) -> None:
    ss = st.session_state
    st.caption("Paste a chat where an AI explained KVL, or upload it as a .txt file. Bifura finds every equation "
               "in it and checks each one against its own derivation.")
    a, b = st.columns([1, 2])
    # write straight into the text box's state (allowed because the box is created below)
    if a.button("Load my example chat (Gemini)"):
        ss.kvl_chat_box = (CIRCUITS / "coupled_inductors_chat.txt").read_text(encoding="utf-8")
    up = b.file_uploader("…or upload a chat (.txt)", type=["txt", "md"], key="kvl_chat_file")
    if up is not None and ss.get("kvl_chat_file_seen") != (up.name, up.size):
        ss.kvl_chat_file_seen = (up.name, up.size)
        ss.kvl_chat_box = up.getvalue().decode("utf-8", errors="replace")
    text = st.text_area("Chat text (paste here)", height=200, key="kvl_chat_box")
    if not st.button("Check this chat", type="primary", disabled=not text.strip()):
        return
    llm = get_llm(settings["provider"]) if settings["ready"] else None
    with st.spinner("Finding the equations and checking them…"):
        found, how = check_chat(text, circuit, llm)
    if not found:
        st.warning("No complete equations ('... = 0') were found in this chat.")
        return
    ai = [f for f in found if f.speaker != "student"]
    wrong_ai = [f for f in ai if not f.check.ok]
    first = wrong_ai[0] if wrong_ai else None
    st.markdown(f"Found **{len(found)}** equations ({how}). "
                f"The AI wrote **{len(ai)}**, and **{len(wrong_ai)}** of them are wrong."
                + (f" **First mistake: message {first.turn}.**" if first and first.turn else ""))
    for i, f in enumerate(found):
        who = {"assistant": "🤖 AI", "student": "🧑‍🎓 Student"}.get(f.speaker, "•")
        head = f"{who} · message {f.turn}" if f.turn else who
        st.markdown(f"**{head}** — {f.context}")
        st.code(f.equation, language=None)
        show_check(f.check, circuit, key=f"chat{i}")


def ask_tab(circuit: Circuit, image: tuple[bytes, str] | None, settings: dict[str, Any]) -> None:
    st.caption("The AI gets the picture and the circuit data and writes the KVL equations (no solving). "
               "Bifura checks them; if they are wrong it tells the AI which terms are wrong and lets it try again.")
    if not settings["ready"]:
        st.error(f"{PROVIDERS[settings['provider']]['label']} is not set up yet.")
        return
    if not st.button(f"Ask {PROVIDERS[settings['provider']]['label']} to write the KVL", type="primary"):
        return
    with st.status("Asking the AI…", expanded=True) as box:
        run = ask_ai_to_write_kvl(circuit, get_llm(settings["provider"]), image, progress=box.write)
        box.update(label="Verified ✓" if run.verified else "Not verified", state="complete" if run.verified else "error",
                   expanded=False)
    if run.error and not run.attempts:
        st.error(f"The AI did not answer: {run.error}")
        return
    for n, att in enumerate(run.attempts):
        st.markdown(f"#### {'First answer' if n == 0 else f'Correction {n}'} ({run.model})")
        if att.reply.get("explanation"):
            st.write(att.reply["explanation"])
        for i, (e, c) in enumerate(zip(att.reply.get("equations") or [], att.checks)):
            st.code(f"Loop {e.get('loop')}: {e.get('equation')}", language=None)
            show_check(c, circuit, key=f"ask{n}-{i}")
    if run.verified:
        st.success(f"✓ Verified: after {len(run.attempts) - 1} correction(s) the AI's KVL matches Bifura's derivation.")
    else:
        st.error("✗ The AI's KVL is still wrong. Do not copy it.")


def own_tab(circuit: Circuit) -> None:
    st.caption("Type a KVL equation the way you would write it, e.g. "
               "`-v1 + R1*i1 + L1*di1/dt - M*d(i1-i2)/dt + L2*d(i1-i2)/dt - M*di1/dt = 0`")
    loop = st.selectbox("Which loop?", ["auto"] + circuit.meshes, key="own_loop")
    text = st.text_input("Your equation", key="own_eq")
    if text.strip():
        show_check(check_equation(text, circuit, None if loop == "auto" else loop), circuit, key="own")


def main_area(settings: dict[str, Any]) -> None:
    st.markdown("## :material/electric_bolt: KVL circuit check")
    st.caption("Bifura derives the correct KVL (mesh) equations itself, using the dot convention for coupled inductors, "
               "then checks equations written by an AI or by you, **term by term**, and explains every wrong term.")
    circuit, image = circuit_section(settings)
    if circuit is None:
        return
    correct_section(circuit)
    st.markdown("### 3 · Check KVL equations")
    t1, t2, t3 = st.tabs([":material/forum: Check a chat I had", ":material/smart_toy: Ask an AI to write KVL",
                           ":material/edit: Check my own equation"])
    with t1:
        chat_tab(circuit, settings)
    with t2:
        ask_tab(circuit, image, settings)
    with t3:
        own_tab(circuit)
