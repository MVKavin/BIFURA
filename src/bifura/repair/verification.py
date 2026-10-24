"""Run the sandbox copy's tests and replay the scenario (fixed commands only)."""

from __future__ import annotations

import difflib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from bifura.analysis.deviation import evaluate_expectations, find_first_deviation
from bifura.tracing.runner import REPO_ROOT, run_agent

TEST_FILE = "test_agent.py"


def run_targeted_tests(workspace: Path, timeout_s: int = 90) -> dict[str, Any]:
    """``python -m pytest -q test_agent.py`` inside the workspace. No caller-supplied command."""
    env = {**os.environ, "PYTHONPATH": str(REPO_ROOT / "src"), "PYTHONIOENCODING": "utf-8"}
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", "-rf", TEST_FILE]
    try:
        proc = subprocess.run(cmd, cwd=workspace, env={**env, "NO_COLOR": "1"}, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout_s)
        out = re.sub(r"\x1b\[[0-9;]*m", "", proc.stdout + proc.stderr)
    except subprocess.TimeoutExpired:
        return {"passed": 0, "failed": 0, "errors": 1, "ok": False, "summary": "test run timed out", "failures": [], "output": ""}
    count = lambda word: sum(int(n) for n in re.findall(rf"(\d+) {word}", out))
    passed, failed, errors = count("passed"), count("failed"), count("error")
    failures = re.findall(r"^FAILED [^:]+::(\S+)(?: - (.*))?$", out, re.M)
    return {"passed": passed, "failed": failed, "errors": errors, "ok": proc.returncode == 0 and passed > 0,
            "summary": (out.strip().splitlines() or ["no output"])[-1][:200],
            "failures": [f"{name}: {msg[:160]}" for name, msg in failures],
            "command": "python -m pytest -q test_agent.py", "output": out[-3000:]}


def replay(workspace: Path, run_id: str) -> dict[str, Any]:
    """Re-run the recorded scenario inputs on the (patched) sandbox copy."""
    env = json.loads((workspace / "scenario_env.json").read_text(encoding="utf-8"))
    run = evaluate_expectations(run_agent(workspace, env, run_id), env)
    dev = find_first_deviation(run, env)
    checks = {e.name: e.event_type == "assertion_passed" for e in run.events if e.event_type.startswith("assertion")}
    return {"run": run, "deviation_found": dev.found, "deviation": dev.description,
            "growth": (run.state or {}).get("growth"), "report": (run.state or {}).get("report"),
            "error": run.error, "checks": checks, "ok": not dev.found and all(checks.values())}


def unified_diff(before: str, after: str, path: str = "agent.py") -> str:
    return "".join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                        fromfile=f"a/{path}", tofile=f"b/{path}"))
