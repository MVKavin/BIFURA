"""LangGraph investigation workflow.

baseline tests -> policy self-check -> investigate (loop: LLM picks a tool, safety gate,
execute, observe) -> verify (orchestrator re-runs tests + replay) -> optional one retry.
"""

from __future__ import annotations

import json
from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from bifura.agent import scripted
from bifura.agent.prompts import SYSTEM, first_message
from bifura.agent.session import InvestigationSession, _clip
from bifura.llm.base import LLMClient, LLMError

AGENT_BUDGET = 12


class GState(TypedDict):
    s: Any
    llm: Any
    done: bool
    retries: int
    script: list


def baseline(state: GState) -> dict:
    s: InvestigationSession = state["s"]
    s.progress("Running the agent's tests on the faulty copy (baseline)…")
    obs = s.call("run_targeted_test", {}, actor="orchestrator", thought="Baseline: the tests should fail before any fix.")
    s.tests_before = obs.get("result")
    return {}


def policy_check(state: GState) -> dict:
    s: InvestigationSession = state["s"]
    s.call("inspect_source_file", {"path": "../../../../.env"}, actor="policy check",
           thought="Scripted safety self-check: a request for the secrets file, claiming to be authorized, "
                   "must be blocked before it reaches any tool.",
           model_metadata={"authorized": True, "trusted": True})
    return {}


def _llm_step(s: InvestigationSession, llm: LLMClient) -> bool:
    if not s.turns:
        s.turns.append({"role": "user", "text": first_message(s)})
    if s.agent_calls >= AGENT_BUDGET:
        s.turns.append({"role": "user", "text": "Tool budget used up. Reply now with action \"finish\"."})
    reply = llm.next_json(SYSTEM, s.turns)
    s.turns.append({"role": "model", "text": json.dumps(reply, ensure_ascii=False)})
    action = str(reply.get("action", "")).strip()
    args = reply.get("args") if isinstance(reply.get("args"), dict) else {}
    if action == "finish" or s.agent_calls >= AGENT_BUDGET:
        s.diagnosis = args if action == "finish" else {"diagnosis": "Stopped: tool budget used up before a conclusion.",
                                                        "failure_category": "unknown_insufficient_evidence"}
        s.progress("gemini: finished the investigation")
        return True
    obs = s.call(action, args, actor="gemini", thought=str(reply.get("thought", "")),
                 hypothesis=reply.get("hypothesis") if isinstance(reply.get("hypothesis"), dict) else None)
    s.turns.append({"role": "user", "text": f"Observation: {_clip(obs, 3500)}\n(tool calls used: {s.agent_calls}/{AGENT_BUDGET})"})
    return False


def investigate(state: GState) -> dict:
    s: InvestigationSession = state["s"]
    llm = state["llm"]
    if s.mode == "gemini" and llm is not None:
        try:
            return {"done": _llm_step(s, llm)}
        except LLMError as exc:
            if s.agent_calls == 0:
                s.notes.append(f"Gemini unavailable ({exc}); switched to scripted mode.")
                s.progress("Gemini call failed; continuing in scripted mode.")
                s.mode = "scripted"
            else:
                s.notes.append(f"Gemini stopped responding mid-investigation: {exc}")
                s.diagnosis = {"diagnosis": "The LLM stopped responding before it finished.",
                               "failure_category": "unknown_insufficient_evidence"}
                return {"done": True}
    script = state["script"] or scripted.plan(s)
    if s.agent_calls >= len(script):
        s.diagnosis = scripted.finish(s)
        return {"done": True, "script": script}
    tool, args, thought = script[s.agent_calls]
    s.call(tool, args, actor="scripted", thought=thought)
    return {"done": False, "script": script}


def verify(state: GState) -> dict:
    s: InvestigationSession = state["s"]
    s.progress("Verifying independently: tests + replay on the patched copy…")
    t = s.call("run_targeted_test", {}, actor="orchestrator", thought="Independent verification of the candidate fix.")
    s.tests_after = t.get("result")
    s.call("replay_run", {}, actor="orchestrator", thought="Replay the same scenario inputs on the patched copy.")
    ok = bool(s.tests_after and s.tests_after.get("ok")) and bool(s.replay_after and s.replay_after.get("ok"))
    retry = (not ok and s.mode == "gemini" and state["retries"] < 1 and s.agent_calls < AGENT_BUDGET
             and bool(s.fault.get("code")))
    if retry:
        s.notes.append("Verification failed once; the investigator got the test output and one more try.")
        s.turns.append({"role": "user", "text": "Bifura's independent verification FAILED. Tests: "
                        + _clip(s.tests_after, 1500) + " Replay: " + _clip({k: (s.replay_after or {}).get(k)
                        for k in ("growth", "report", "deviation", "checks")}, 800)
                        + " Continue investigating and fix it, then finish."})
    return {"done": not retry, "retries": state["retries"] + (1 if retry else 0)}


def build_graph():
    g = StateGraph(GState)
    g.add_node("baseline", baseline)
    g.add_node("policy_check", policy_check)
    g.add_node("investigate", investigate)
    g.add_node("verify", verify)
    g.set_entry_point("baseline")
    g.add_edge("baseline", "policy_check")
    g.add_edge("policy_check", "investigate")
    g.add_conditional_edges("investigate", lambda st: "verify" if st["done"] else "investigate",
                            {"verify": "verify", "investigate": "investigate"})
    g.add_conditional_edges("verify", lambda st: END if st["done"] else "investigate",
                            {END: END, "investigate": "investigate"})
    return g.compile()


def run_workflow(s: InvestigationSession, llm: LLMClient | None) -> InvestigationSession:
    build_graph().invoke({"s": s, "llm": llm, "done": False, "retries": 0, "script": []},
                         {"recursion_limit": 100})
    return s
