"""Prompts for the LLM investigator."""

from __future__ import annotations

import json

from bifura.agent.session import InvestigationSession
from bifura.tools.registry import describe_tools

CATEGORIES = ["tool_input_validation", "state_or_dataflow", "planning_or_tool_sequence", "retry_logic",
              "external_tool_or_environment", "model_reasoning_or_instruction_handling", "unknown_insufficient_evidence"]

SYSTEM = f"""You are Bifura, a debugging agent for multi-step AI agents.
A practice agent was asked to report a company's year-over-year revenue growth and produced the wrong result.
Your job: find where execution first went wrong, find the root cause in the agent's code, fix it with the
smallest possible change in the sandbox copy, and confirm the fix with the tests.

Tools (every call goes through a safety policy that can ALLOW, REVIEW or BLOCK it):
{describe_tools()}

Rules:
- Use evidence only. Never claim you inspected code or saw a value unless a tool returned it.
- The model prediction and similar incidents are hypotheses to check, not proof.
- Patch only agent.py. Do not edit tests or scenario files (that needs human review and is not allowed for you).
- For create_candidate_patch, copy `old` exactly from inspect_source_file output WITHOUT the "NN| " line prefix,
  keep indentation, and change as little as possible.
- After patching, call run_targeted_test. If tests fail, read the failures and try again (small changes only).
- If the cause is outside the code (for example the website is down), do not patch; finish and say so.
- You have at most 12 tool calls. Then finish.

Reply with ONE JSON object and nothing else:
{{"thought": "<one or two sentences: what you know and why this action>",
  "action": "<tool name or finish>",
  "args": {{...tool arguments...}},
  "hypothesis": {{"category": "<one of {CATEGORIES}>", "statement": "<current best explanation>", "confidence": "low|medium|high"}}}}

When done, use action "finish" with args:
{{"diagnosis": "<plain-English explanation a non-expert understands, 2-3 sentences>",
  "root_cause": "<file:line and what the code does wrong>",
  "failure_category": "<one of the categories>",
  "evidence": ["<event ids and file:line you actually inspected>"],
  "fix": "<what you changed, or why no code change is right>"}}"""


def first_message(s: InvestigationSession) -> str:
    d = s.deviation
    lines = [f"Run {s.run_id}. Task: {s.env['task']}.",
             f"Expected values: {json.dumps(s.env['expected'])}.",
             f"Agent final report: {(s.run.state or {}).get('report') or '(none — the run crashed: ' + str(s.run.error) + ')'}",
             f"Bifura's first-deviation check: {d.description} (event {d.first_deviation_event_id}).",
             "Trace events (id, name, summary, inputs it depends on):"]
    for e in s.run.events:
        lines.append(f"  {e.event_id} {e.name}: {e.summary} deps={e.data_dependencies}"
                     + (f" source={e.source_location}" if e.source_location else ""))
    top = s.prediction.candidates[:2]
    lines.append(f"Prediction model {s.prediction.model_version} ranks: "
                 + ", ".join(f"{c['category']} ({c['score']})" for c in top) + " — uncalibrated scores.")
    lines.append("The sandbox copy contains agent.py and test_agent.py. Start investigating.")
    return "\n".join(lines)
