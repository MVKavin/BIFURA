"""Registered investigation/repair tools and their argument schemas.

Only tools listed here can ever be executed. The schema is checked by the safety
policy before anything runs.
"""

from __future__ import annotations

from typing import Any

# name -> {"args": {arg: (type, required)}, "access": read|write|run, "description": str}
TOOLS: dict[str, dict[str, Any]] = {
    "get_run_summary": {"args": {}, "access": "read",
                        "description": "Task, expectations, status, first deviation and the event list."},
    "get_trace_event": {"args": {"event_id": (str, True)}, "access": "read",
                        "description": "Full input, output, state change, error and source location of one event."},
    "inspect_source_file": {"args": {"path": (str, True), "start_line": (int, False), "end_line": (int, False)},
                            "access": "read", "description": "Read lines of a file in the run's sandbox copy, with line numbers."},
    "search_source": {"args": {"query": (str, True)}, "access": "read",
                      "description": "Find lines containing text in the sandbox copy of the agent."},
    "get_prediction": {"args": {}, "access": "read",
                       "description": "The trained model's ranked failure categories for this trace (a hypothesis, not proof)."},
    "retrieve_incidents": {"args": {}, "access": "read",
                           "description": "Similar past incidents from incident memory, with matched features."},
    "create_candidate_patch": {"args": {"path": (str, True), "old": (str, True), "new": (str, True),
                                        "hypothesis": (str, False)},
                               "access": "write", "description": "Replace one exact snippet in a sandbox file. Never touches the real project."},
    "run_targeted_test": {"args": {}, "access": "run",
                          "description": "Run the agent's test file in the sandbox copy (fixed command; no arguments)."},
    "replay_run": {"args": {}, "access": "run",
                   "description": "Re-run the same scenario on the sandbox copy and compare with expectations."},
}

# Files or folders that may never be read or written, even inside the workspace.
PROTECTED_NAMES = {".env", ".git", ".venv", "id_rsa", "id_ed25519", "secrets", "secrets.txt", "credentials.json"}
# Patching these could make verification meaningless, so a human must approve.
REVIEW_REQUIRED_FILES = {"test_agent.py", "scenario_env.json"}


def describe_tools() -> str:
    lines = []
    for name, spec in TOOLS.items():
        args = ", ".join(f"{a}{'' if req else '?'}: {t.__name__}" for a, (t, req) in spec["args"].items())
        lines.append(f"- {name}({args}): {spec['description']}")
    return "\n".join(lines)
