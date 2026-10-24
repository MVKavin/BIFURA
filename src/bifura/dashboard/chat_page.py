"""Streamlit "Chat check" mode: chat with Gemini / GPT / Claude while Bifura checks every step."""

from __future__ import annotations

from typing import Any

import streamlit as st

from bifura.chatcheck.record import load_chat, save_chat_run
from bifura.chatcheck.session import EXAMPLES, run_chat_check
from bifura.llm import PROVIDERS, get_llm, provider_status

ICON = {"ok": "✅", "wrong": "❌", "affected": "⚠️", "unverifiable": "❔"}
WORD = {"ok": "correct", "wrong": "WRONG (first mistake)", "affected": "wrong because of an earlier step",
        "unverifiable": "could not check"}


def sidebar_settings() -> dict[str, Any]:
    """Chat-check settings shown in the sidebar."""
    st.markdown("#### 1 · Pick the AI to check")
    statuses = {p: provider_status(p) for p in PROVIDERS}
    options = list(PROVIDERS)
    default = next((i for i, p in enumerate(options) if statuses[p].ready), 0)
    provider = st.radio("AI model", options, index=default, key="chat_provider",
                        format_func=lambda p: PROVIDERS[p]["label"] + ("" if statuses[p].ready else "  (not set up)"))
    if not statuses[provider].ready:
        st.warning(statuses[provider].message, icon=":material/warning:")
        with st.expander(f"How to add {PROVIDERS[provider]['label']}"):
            key = PROVIDERS[provider]["keys"][0]
            pkg = {"gemini": "", "gpt": "pip install openai", "claude": "pip install anthropic"}[provider]
            st.markdown(f"1. Get an API key from the provider's website.\n"
                        f"2. Open `.env` and add a line: `{key}=your_key`\n"
                        + (f"3. In the terminal run: `{pkg}`\n" if pkg else "")
                        + "4. Restart Streamlit.")
    st.markdown("#### 2 · Options")
    demo = st.toggle("Demo: make the AI slip one mistake", value=False, key="chat_demo",
                     help="Asks the AI to put one realistic calculation slip in its answer, so you can show Bifura "
                          "catching it. Clearly labelled in the results.")
    expected = st.text_input("Expected final answer (optional)", key="chat_expected",
                             placeholder="e.g. 16 W", help="Like a teacher's answer key. Lets Bifura also catch a wrong formula.")
    return {"provider": provider, "ready": statuses[provider].ready, "demo": demo, "expected": expected.strip() or None}


def _steps_table(steps: list[dict[str, Any]]) -> None:
    rows = []
    for s in steps:
        val = "—" if s["claimed"] is None else f"{s['claimed']:g}"
        rows.append({"": ICON.get(s["status"], "•"), "Step": s["n"], "What": s["explanation"][:60],
                     "Calculation": f"{s['name']} = {s['formula']}", "AI wrote": val,
                     "Bifura check": WORD.get(s["status"], s["status"]) + (f" — {s['note']}" if s["note"] else "")})
    st.dataframe(rows, hide_index=True, use_container_width=True)


def show_result(t: dict[str, Any]) -> None:
    with st.chat_message("user"):
        st.write(t["question"])
        if t.get("expected"):
            st.caption(f"Expected answer: {t['expected']}")
    first = t["attempts"][0] if t["attempts"] else None
    with st.chat_message("assistant", avatar=":material/smart_toy:"):
        st.markdown(f"**{t['label']}** ({t['model']})" + ("  ·  _demo: asked to slip one mistake_" if t.get("demo_slip") else ""))
        if not first:
            st.error(f"The AI did not answer: {t.get('error')}")
            return
        st.write(first["solution"].get("answer_text") or "")
        _steps_table(first["steps"])
    wrong = next((s for s in first["steps"] if s["status"] == "wrong"), None)
    affected = [s for s in first["steps"] if s["status"] == "affected"]
    with st.chat_message("assistant", avatar=":material/call_split:"):
        st.markdown("**Bifura's check**")
        for p in first["given_problems"]:
            st.error(f"Copied a wrong number from the question: {p}")
        if wrong:
            # formulas go in code style so "*" is shown, not read as markdown bold/italic
            st.error(f"**First wrong step: step {wrong['n']} ({wrong['name']}).** Recalculating: `{wrong['note']}`")
            st.markdown(f"- **Likely type of mistake:** {wrong['mistake_type']} _(rule-based guess)_\n"
                        + (f"- **Spoiled later steps:** " + ", ".join(f"step {s['n']} ({s['name']})" for s in affected) + "\n"
                           if affected else "")
                        + "- Everything before this step was correct.")
        elif first["ok"]:
            st.success("Every step recalculates correctly. Nothing to fix.")
        else:
            st.warning("Some steps could not be checked or the final answer does not match the expected answer.")
        if t["corrected"]:
            last = t["attempts"][-1]
            st.markdown(f"**Bifura asked {t['label']} to correct itself** ({len(t['attempts']) - 1} round(s)). Corrected answer:")
            _steps_table(last["steps"])
            if t["verified"]:
                st.success("✓ Verified: every step of the corrected answer recalculates correctly"
                           + (f" and matches {t['expected']}." if t.get("expected") else "."))
            else:
                st.error("✗ Still wrong after the correction attempts. Do not trust this answer.")
        st.button("Watch it in the story view", icon=":material/play_circle:", key=f"story-{t['run_id']}", on_click=_open_story, args=(t["run_id"],))


def _open_story(run_id: str) -> None:
    """Switch to the story view on this chat run (callback: runs before widgets are drawn)."""
    st.session_state.view_radio = "agent"
    st.session_state.active, st.session_state.autoplay = run_id, True
    st.session_state.open_chat = run_id  # show this chat run in the agent view's run list
    st.cache_data.clear()  # so the run list includes this new chat run


def main_area(settings: dict[str, Any]) -> None:
    st.markdown("## :material/calculate: Numeric chat check")
    st.caption("Ask Gemini, GPT or Claude a numerical problem (circuits, physics, maths). The AI answers step by step; "
               "Bifura recalculates every step exactly, finds the **first** wrong step, asks the AI to fix it, "
               "and checks the fix. Bifura proves calculation mistakes; give an expected answer to also catch a wrong formula.")
    ss = st.session_state
    ss.setdefault("chat_ids", [])
    for run_id in ss.chat_ids:
        t = load_chat(run_id)
        if t:
            show_result(t)

    st.markdown("**Try an example:**")
    cols = st.columns(len(EXAMPLES))
    clicked = None
    for col, (label, q) in zip(cols, EXAMPLES.items()):
        if col.button(label, key=f"ex-{label}", use_container_width=True):
            clicked = q
    question = st.chat_input("Type a numerical problem for the AI…") or clicked
    if not question:
        return
    if not settings["ready"]:
        st.error(f"{PROVIDERS[settings['provider']]['label']} is not set up yet. See the sidebar.")
        return
    llm = get_llm(settings["provider"])
    with st.status(f"Asking {PROVIDERS[settings['provider']]['label']}…", expanded=True) as box:
        run = run_chat_check(question, llm, settings["provider"], demo_slip=settings["demo"],
                             expected=settings["expected"], progress=box.write)
        if not run.attempts:
            box.update(label="The AI did not answer", state="error", expanded=False)
    if not run.attempts:
        busy = any(w in (run.error or "") for w in ("busy", "503", "UNAVAILABLE", "high demand", "rate"))
        st.error(("The AI's servers are overloaded right now. Wait a minute and try again.\n\n" if busy else "")
                 + f"Details: {run.error or 'no answer'}")
        return
    with st.status("Saving the check…", expanded=False) as box:
        t = save_chat_run(run)
        box.update(label="Verified ✓" if t["verified"] else ("Mistake found and not fixed" if t["corrected"] or not t["attempts"][0]["ok"] else "Checked"),
                   state="complete" if t["verified"] else "error")
    ss.chat_ids.append(t["run_id"])
    st.rerun()
