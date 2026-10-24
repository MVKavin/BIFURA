"""Prepare sandbox copies of the practice agent, inject faults, and run them traced."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import shutil
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from bifura.schemas.models import TraceEvent
from bifura.sdk import Tracer

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = Path(os.environ.get("BIFURA_DATA_DIR") or REPO_ROOT / "data")
if not DATA_DIR.is_absolute():
    DATA_DIR = REPO_ROOT / DATA_DIR
SANDBOX = DATA_DIR / "sandbox"
AGENT_DIR = SANDBOX / "practice_agent"
RUNTIME = SANDBOX / "runtime"
AGENT_FILES = ("agent.py", "test_agent.py")


def load_faults() -> dict[str, dict[str, Any]]:
    data = json.loads((SANDBOX / "faults.json").read_text(encoding="utf-8"))
    return {f["id"]: f for f in data["faults"]}


def load_scenarios() -> dict[str, dict[str, Any]]:
    data = json.loads((SANDBOX / "scenarios.json").read_text(encoding="utf-8"))
    return {s["id"]: s for s in data["scenarios"]}


def apply_fault_env(env: dict[str, Any], fault: dict[str, Any] | None) -> dict[str, Any]:
    """Return a copy of ``env`` with the fault's environment conditions applied."""
    env = copy.deepcopy(env)
    over = (fault or {}).get("env") or {}
    if "url_suffix" in over:
        env["url"] = env["url"] + over["url_suffix"]
    if "page" in over:
        env["pages"] = {**env["pages"], env["url"]: over["page"]}
    return env


def inject(source: str, replacements: list[dict[str, str]]) -> str:
    """Apply exact, single-occurrence text replacements (fault injection or a patch)."""
    for r in replacements:
        count = source.count(r["old"])
        if count != 1:
            raise ValueError(f"expected exactly one match for {r['old']!r}, found {count}")
        source = source.replace(r["old"], r["new"])
    return source


def prepare_workspace(run_id: str, fault: dict[str, Any] | None, env: dict[str, Any],
                      root: Path | None = None) -> Path:
    """Copy the clean agent into a disposable runtime folder and inject the fault."""
    ws = (root or RUNTIME) / run_id
    if ws.exists():
        try:
            shutil.rmtree(ws)
        except OSError:  # e.g. OneDrive/antivirus holding a file: use a fresh folder instead
            ws = ws.with_name(f"{run_id}-{uuid.uuid4().hex[:6]}")
    ws.mkdir(parents=True)
    for name in AGENT_FILES:
        shutil.copy2(AGENT_DIR / name, ws / name)
    if fault and fault.get("code"):
        agent_py = ws / "agent.py"
        agent_py.write_text(inject(agent_py.read_text(encoding="utf-8"), fault["code"]), encoding="utf-8")
    (ws / "scenario_env.json").write_text(json.dumps(env, ensure_ascii=False, indent=2), encoding="utf-8")
    return ws


def load_agent(workspace: Path):
    """Import agent.py from a workspace under a unique module name (no caching between runs)."""
    spec = importlib.util.spec_from_file_location(f"bifura_agent_{uuid.uuid4().hex}", workspace / "agent.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


@dataclass
class AgentRun:
    run_id: str
    events: list[TraceEvent]
    state: dict[str, Any] | None
    error: str | None = None
    error_type: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def crashed(self) -> bool:
        return self.error is not None


def run_agent(workspace: Path, env: dict[str, Any], run_id: str) -> AgentRun:
    """Run the agent in ``workspace`` with the instrumentation SDK attached."""
    tracer = Tracer(run_id)
    try:
        agent = load_agent(workspace)
        state = agent.run(env, tracer)
        return AgentRun(run_id, tracer.events, state)
    except Exception as exc:  # the trace still holds everything up to the failure
        return AgentRun(run_id, tracer.events, None, str(exc), type(exc).__name__)
