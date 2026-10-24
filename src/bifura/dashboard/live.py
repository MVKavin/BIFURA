"""Story text for live investigations, built from the saved investigation transcript.

All text that came from the LLM or the trace is HTML-escaped here, because the
template inserts narrative fields as HTML.
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any

from bifura.tracing.runner import REPO_ROOT

INVESTIGATIONS = REPO_ROOT / "results" / "investigations"


def chat_narrative(t: dict[str, Any]) -> dict[str, Any]:
    """Story text for a Chat check run (an AI's step-by-step answer checked by Bifura)."""
    e = escape
    who = f"{t['label']} ({t['model']})"
    first, last = t["attempts"][0], t["attempts"][-1]
    wrong = next((s for s in first["steps"] if s["status"] == "wrong"), None)
    affected = [s for s in first["steps"] if s["status"] == "affected"]
    fixed_by_name = {s["name"]: s for s in last["steps"]}
    verified, corrected = t["verified"], t["corrected"]
    f = lambda x: "—" if x is None else f"{x:g}"
    nr: dict[str, Any] = {
        "titles": {"code": "Pinpoint the wrong calculation", "fix": "Ask the AI to correct itself",
                   "replay": "Recalculate the corrected answer"},
        "dig_label": "See the wrong calculation",
        "fix_now": "Asking the AI to redo it",
        "say": {"compare": f"{e(who)} answered step by step. Bifura recalculates every step with an exact calculator."
                           + (" One step does not add up." if wrong else ""),
                "fix": f"Bifura tells {e(t['label'])} exactly which step is wrong and asks it to redo the solution.",
                "verdict": ("The corrected answer checks out: every step now recalculates correctly." if verified and corrected
                            else "The AI's answer was already correct." if verified else
                            "The AI did not fix it. Bifura reports the answer as still wrong.")},
        "tech": {"fix": e(f"correction request → {t['label']} · recalculation with SymPy")},
        "find": {"fix": e(f"{len(t['attempts']) - 1} correction round(s) · {'all steps check out' if verified else 'still wrong'}")},
        "summary": f"{t['run_id']}: {who}. " + (f"First wrong step {wrong['n']} ({wrong['name']}): {wrong['note']}. " if wrong else "")
                   + ("Corrected and verified." if verified and corrected else "Correct first time." if verified else "Not fixed."),
        "nodes": {}, "result_rows": [],
    }
    if wrong:
        nr["dev_line"] = "its calculation does not add up"
        nr["io"] = [["recalculated", f(wrong["recomputed"])], [f"{e(t['label'])} wrote", f(wrong["claimed"])]]
        nr["say"]["dev"] = (f"Found it. In step {wrong['n']}, {e(wrong['formula'])} gives <b>{f(wrong['recomputed'])}</b>, "
                            f"but the AI wrote <span class=\"x\">{f(wrong['claimed'])}</span>. Every step before it was right.")
        nr["say"]["code"] = f"Step {wrong['n']}: {e(wrong['name'])} = {e(wrong['formula'])}. Likely a {e(wrong['mistake_type'] or 'slip')}."
        nr["find"]["code"] = e(f"step {wrong['n']}: {wrong['name']} = {f(wrong['claimed'])}, should be {f(wrong['recomputed'])}")
        if affected:
            nr["say"]["impact"] = (f"One wrong number, {len(affected)} more wrong step(s). "
                                   f"Everything after step {wrong['n']} inherited it.")
        lines = [[s["n"], f"{s['name']} = {s['formula']} = {f(s['claimed'])}"] for s in first["steps"]]
        fix_step = fixed_by_name.get(wrong["name"])
        nr["code"] = {"file": "the AI's solution", "hit": wrong["n"], "lines": lines,
                      "bug": f"{wrong['name']} = {wrong['formula']} = {f(wrong['claimed'])}",
                      "fix": (f"{fix_step['name']} = {fix_step['formula']} = {f(fix_step['claimed'])}" if fix_step and corrected
                              else f"{wrong['name']} = {wrong['formula']} = {f(wrong['recomputed'])}"),
                      "evidence": [f'<span class="g">+</span> recalculated: {e(wrong["formula"])} = {f(wrong["recomputed"])}',
                                   f'<span class="x">−</span> the AI wrote {f(wrong["claimed"])}',
                                   f'<span class="g">+</span> likely mistake type: {e(wrong["mistake_type"] or "slip")} (rule-based guess)']}
        nr["code_dig"] = f"Walk through step {wrong['n']}"
        nr["replay"] = {"applied": "AI's corrected answer received", "tests_label": "steps",
                        "before": f"before  {e(wrong['name'])} = <span class=\"x\">{f(wrong['claimed'])}</span>",
                        "after": (f"after   {e(wrong['name'])} = <span class=\"g\">{f(fix_step['claimed'])}</span>" if fix_step
                                  else "after   no corrected answer")}
        nr["nodes"][t["step_events"][wrong["name"]]] = {
            "what": f"The AI computed {e(wrong['name'])} with {e(wrong['formula'])}. Recalculating that gives {f(wrong['recomputed'])}, "
                    f"but it wrote {f(wrong['claimed'])}. This is the first step that does not add up.",
            "fixed": f"In the corrected answer, {e(wrong['name'])} = {f(fix_step['claimed']) if fix_step else '?'}.",
            "ex": [f(wrong["recomputed"]), f(wrong["claimed"])]}
    for s in first["steps"]:
        ev = t["step_events"].get(s["name"])
        fx = fixed_by_name.get(s["name"])
        if ev and fx and verified:
            nr["nodes"].setdefault(ev, {})["fixed_sub"] = f"{s['name']} = {f(fx['claimed'])}"
        if ev and s["status"] == "affected":
            nr["nodes"].setdefault(ev, {}).update({
                "what": f"This step's own arithmetic is right, but it used a wrong earlier number. "
                        f"With correct inputs it should be {f(s['true_value'])}.",
                "ex": [f(s["true_value"]), f(s["claimed"])], "impact": "used the wrong number"})
    rows = [["v" if verified else "h", "verified" if verified else "not verified",
             e("Every step of the final answer recalculates correctly." if verified else "The final answer still has wrong steps.")],
            ["", "AI", e(f"{who} answered" + (f" and corrected itself after {len(t['attempts']) - 1} request(s)." if corrected else "."))]]
    if wrong:
        rows.append(["", "mistake", e(f"Step {wrong['n']}: {wrong['mistake_type']} (rule-based guess)")])
    if t.get("expected"):
        rows.append(["", "answer key", e(f"Compared with your expected answer: {t['expected']}")])
    if t.get("demo_slip"):
        rows.append(["h", "demo", "The AI was asked to slip one mistake on purpose, to demonstrate the check."])
    rows.append(["h", "limit", "Bifura proves calculation mistakes. A wrong formula choice is only caught if you give the expected answer."])
    nr["result_rows"] = rows
    return nr


def load_transcript(run_id: str) -> dict[str, Any] | None:
    path = INVESTIGATIONS / f"{run_id}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def _args(args: dict[str, Any]) -> str:
    if "start_line" in args:
        return f"{args.get('path')} {args.get('start_line')}–{args.get('end_line', '')}"
    if "event_id" in args:
        return str(args["event_id"])
    if "old" in args:
        return str(args.get("path"))
    return ", ".join(f"{k}={str(v)[:20]}" for k, v in args.items())


def investigator_name(t: dict[str, Any]) -> str:
    return f"Gemini ({t.get('llm_model')})" if t.get("mode") == "gemini" else "Scripted investigator"


def live_narrative(t: dict[str, Any], deviation_event_id: str | None) -> dict[str, Any]:
    who = investigator_name(t)
    short = "Gemini" if t.get("mode") == "gemini" else "Script"
    diag = t.get("diagnosis") or {}
    steps = t.get("steps") or []
    agent_steps = [s for s in steps if s["actor"] in ("gemini", "scripted")]
    blocked = [s for s in steps if s["decision"] in ("BLOCK", "REVIEW")]
    tb, ta = t.get("tests_before") or {}, t.get("tests_after") or {}
    verified = bool(t.get("verified"))
    e = escape

    bullets = []
    for s in agent_steps[:9]:
        mark = '<span class="g">+</span>' if s["decision"] == "ALLOW" else '<span class="x">−</span>'
        verdict = {"ALLOW": "allowed", "BLOCK": "blocked", "REVIEW": "held for review"}[s["decision"]]
        bullets.append(f"{mark} {e(short)} → <b>{e(s['action'])}</b>({e(_args(s['args']))}) · {verdict}")
    hyps = [s["hypothesis"] for s in agent_steps if s.get("hypothesis")]
    if hyps:
        h = hyps[-1]
        bullets.append(f'<span class="g">+</span> hypothesis ({e(str(h.get("confidence", "?")))}): {e(str(h.get("statement", "")))}')

    nr: dict[str, Any] = {
        "dig_label": "See what went wrong here",
        "say": {"verdict": e(diag.get("diagnosis") or "") + (" The fix passes the tests and the replay." if verified
                                                            else " The fix is not verified.")},
        "tech": {"code": e(" · ".join(f"{s['action']}:{s['decision']}" for s in agent_steps[:8]))},
        "find": {},
        "summary": f"{t['run_id']}: {diag.get('diagnosis', '')} Root cause: {diag.get('root_cause', 'n/a')}. "
                   f"{'Verified by tests and replay.' if verified else 'Not verified.'} Investigator: {who}.",
        "nodes": {},
    }
    if diag.get("root_cause"):
        nr["find"]["code"] = e(diag["root_cause"])
        nr["say"]["code"] = f"{e(who)} reads the code. {e(diag['root_cause'])}"

    patches = t.get("patches") or []
    if patches:
        p = patches[0]
        src = (t.get("original_source") or "").splitlines()
        hit, span = p["line"], p["old"].count("\n")
        lo, hi = max(1, hit - 4), min(len(src), hit + span + 3)
        total = int(tb.get("passed", 0)) + int(tb.get("failed", 0))
        first_fail = (tb.get("failures") or [""])[0]
        nr["code"] = {"file": p["path"], "hit": hit, "lines": [[i, src[i - 1]] for i in range(lo, hi + 1)],
                      "bug": p["old"], "fix": p["new"], "evidence": bullets,
                      "test": {"name": "test_agent.py",
                               "before": f"{tb.get('failed', 0)} of {total} tests failed before the fix. {first_fail[:140]}"}}
        nr["code_dig"] = f"Walk through {e(p['path'])}:{hit}"
    elif bullets:
        nr["code"] = {"file": "agent.py", "hit": 0, "lines": [], "bug": "", "fix": "", "evidence": bullets}

    if deviation_event_id:
        ev = [["bulb", f"{e(who)} hypothesis", e(str(h.get("statement", "")))] for h in hyps[-2:]]
        nr["nodes"][deviation_event_id] = {"evidence": ev} if ev else {}
    if verified:
        for eid, info in (t.get("replay_events") or {}).items():
            nr["nodes"].setdefault(eid, {})["fixed_sub"] = str(info.get("summary") or "")[:40]

    pred_ok = t.get("category_correct")
    rows = [["v" if verified else "h", "verified" if verified else "not verified",
             e(f"Tests {ta.get('summary', 'not run')}; replay {(t.get('replay') or {}).get('growth')}% growth.")],
            ["", "investigator", e(f"{who} used {len(agent_steps)} tool calls; {len(blocked)} action(s) stopped by the safety policy.")],
            ["", "diagnosis", e(f"{diag.get('failure_category', 'unknown')}"
                               + (" — matches the injected fault's true category." if pred_ok else " — differs from the injected fault's true category."))],
            ["", "learning", e(f"Saved as INC-{t['run_id']} ({'verified' if verified else 'suspected'}). "
                               "It can train the model only after a human approves it.")]]
    if t.get("notes"):
        rows.append(["h", "note", e(" ".join(t["notes"]))])
    nr["result_rows"] = rows
    return nr
