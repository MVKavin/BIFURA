"""Safety policy evaluator: decides ALLOW, REVIEW or BLOCK for a proposed tool call.

Pure and deterministic: it never runs a tool. Authorization comes only from the
trusted ``context`` built by the orchestrator. Anything the model puts in the
proposal (for example ``model_generated_metadata={"authorized": True}``) is ignored.
"""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from bifura.schemas.models import (
    ExecutionStatus,
    SafetyDecisionRecord,
    SafetyDecisionType,
    ToolCallProposal,
)
from bifura.tools.registry import PROTECTED_NAMES, REVIEW_REQUIRED_FILES, TOOLS

POLICY_VERSION = "1.0"
REQUIRED_CONTEXT = ("workspace_root", "sandbox_root", "allowed_tools", "permissions", "provenance", "mode")


def _decision(proposal: ToolCallProposal, kind: SafetyDecisionType, rule: str, reason: str,
              target: str | None = None) -> SafetyDecisionRecord:
    status = {SafetyDecisionType.ALLOW: ExecutionStatus.NOT_STARTED,
              SafetyDecisionType.REVIEW: ExecutionStatus.AWAITING_REVIEW,
              SafetyDecisionType.BLOCK: ExecutionStatus.BLOCKED_BEFORE_EXECUTION}[kind]
    return SafetyDecisionRecord(
        decision_id=f"dec-{uuid.uuid4().hex[:10]}", decision=kind, proposal_id=proposal.proposal_id,
        tool_call_id=proposal.tool_call_id, run_id=proposal.run_id, policy_rule=rule, rule_ids=[rule],
        reason=reason, policy_version=POLICY_VERSION, validated_target=target, execution_status=status,
        review_status="pending" if kind == SafetyDecisionType.REVIEW else "not_required")


def _resolve_inside(root: str, rel: str) -> Path | None:
    """Resolve ``rel`` under ``root``; None if it escapes the root."""
    base = Path(root).resolve()
    target = (base / rel).resolve()
    try:
        target.relative_to(base)
    except ValueError:
        return None
    return target


def evaluate_tool_action(proposal: ToolCallProposal, context: dict[str, Any]) -> SafetyDecisionRecord:
    """Evaluate one proposal against the mandatory rules. Never executes anything."""
    allow, review, block = SafetyDecisionType.ALLOW, SafetyDecisionType.REVIEW, SafetyDecisionType.BLOCK
    missing = [k for k in REQUIRED_CONTEXT if k not in context]
    if missing:
        return _decision(proposal, block, "trusted_context_required", f"Trusted context missing: {', '.join(missing)}.")

    spec = TOOLS.get(proposal.tool_name)
    if spec is None:
        return _decision(proposal, block, "unregistered_tool", f"'{proposal.tool_name}' is not a registered tool.")
    if proposal.tool_name not in context["allowed_tools"]:
        return _decision(proposal, block, "tool_not_allowed", f"'{proposal.tool_name}' is not allowed in this run.")

    args = proposal.arguments or {}
    unknown = set(args) - set(spec["args"])
    if unknown:
        rule = "no_shell_or_command" if unknown & {"command", "cmd", "shell", "args"} else "schema_validation"
        return _decision(proposal, block, rule, f"Unexpected argument(s): {', '.join(sorted(unknown))}.")
    for name, (typ, required) in spec["args"].items():
        if required and name not in args:
            return _decision(proposal, block, "schema_validation", f"Missing required argument '{name}'.")
        if name in args and not isinstance(args[name], typ):
            return _decision(proposal, block, "schema_validation", f"Argument '{name}' must be {typ.__name__}.")

    budget = context.get("budget") or {}
    if budget and budget.get("used", 0) >= budget.get("max_calls", 10**9):
        return _decision(proposal, block, "action_budget", f"Tool budget of {budget['max_calls']} calls is used up.")

    target = None
    if "path" in args:
        parts = {p.lower() for p in Path(args["path"]).parts}
        if parts & PROTECTED_NAMES:
            return _decision(proposal, block, "protected_file", f"'{args['path']}' is a protected file.")
        root = context["sandbox_root"] if spec["access"] == "write" else context["workspace_root"]
        resolved = _resolve_inside(root, args["path"])
        if resolved is None:
            return _decision(proposal, block, "workspace_containment",
                             f"'{args['path']}' resolves outside the permitted workspace.")
        target = str(resolved)

    perms = context["permissions"]
    if spec["access"] == "write":
        if perms.get("write_project"):
            return _decision(proposal, block, "no_project_writes", "Project writes are never permitted.")
        if not perms.get("write_sandbox"):
            return _decision(proposal, block, "sandbox_write_not_authorized", "Sandbox writes are not authorized for this run.")
        if Path(args["path"]).name in REVIEW_REQUIRED_FILES:
            return _decision(proposal, review, "test_or_fixture_change_needs_review",
                             f"Changing {Path(args['path']).name} could weaken verification; a human must approve.", target)
    if spec["access"] == "run" and not perms.get("run_tests", True):
        return _decision(proposal, block, "test_runs_not_authorized", "Running tests is not authorized for this run.")

    return _decision(proposal, allow, "registered_tool_within_scope", "Registered tool, valid arguments, target inside scope.", target)
