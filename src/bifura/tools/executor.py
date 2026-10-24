"""Central tool executor: the only route from a proposal to a tool implementation.

Fail-closed: a handler runs only after the evaluator returns a valid ALLOW decision
for this exact proposal. BLOCK, REVIEW, a missing evaluator, an evaluator error or
an invalid decision all mean the handler is never called.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from typing import Any

from bifura.schemas.models import (
    ExecutionStatus,
    SafetyDecisionRecord,
    SafetyDecisionType,
    ToolCallProposal,
    ToolExecutionResult,
)
from bifura.tools.policy import evaluate_tool_action

Handler = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]
Evaluator = Callable[[ToolCallProposal, dict[str, Any]], SafetyDecisionRecord]


def _fail_closed(proposal: ToolCallProposal) -> SafetyDecisionRecord:
    return SafetyDecisionRecord(
        decision_id=f"dec-{uuid.uuid4().hex[:10]}", decision=SafetyDecisionType.BLOCK,
        proposal_id=proposal.proposal_id, run_id=proposal.run_id, policy_rule="fail_closed_guard",
        rule_ids=["fail_closed_guard"], reason="Evaluator missing, threw exception, or returned invalid decision.",
        execution_status=ExecutionStatus.BLOCKED_BEFORE_EXECUTION)


def _not_run(proposal: ToolCallProposal, decision: SafetyDecisionRecord, why: str) -> ToolExecutionResult:
    return ToolExecutionResult(proposal_id=proposal.proposal_id, decision_id=decision.decision_id, executed=False,
                               success=False, error_type="SafetyBlockError", error_message=why)


def execute_tool_action(proposal: ToolCallProposal, context: dict[str, Any],
                        evaluator: Evaluator | None = evaluate_tool_action,
                        handlers: dict[str, Handler] | None = None) -> tuple[SafetyDecisionRecord, ToolExecutionResult]:
    """Evaluate, then execute only on ALLOW. Returns (decision, result); the decision is never edited."""
    try:
        if evaluator is None:
            raise RuntimeError("no evaluator")
        decision = evaluator(proposal, context)
        if not isinstance(decision, SafetyDecisionRecord) or decision.proposal_id != proposal.proposal_id:
            raise RuntimeError("invalid decision")
    except Exception:
        decision = _fail_closed(proposal)
        return decision, _not_run(proposal, decision, "Execution blocked by safety policy or evaluator failure.")

    if decision.decision == SafetyDecisionType.BLOCK:
        return decision, _not_run(proposal, decision, f"Blocked: {decision.reason}")
    if decision.decision == SafetyDecisionType.REVIEW:
        return decision, ToolExecutionResult(proposal_id=proposal.proposal_id, decision_id=decision.decision_id,
                                             executed=False, success=None, error_type="AwaitingReview",
                                             error_message=f"Waiting for human review: {decision.reason}")
    if decision.decision != SafetyDecisionType.ALLOW:
        decision = _fail_closed(proposal)
        return decision, _not_run(proposal, decision, "Unknown decision type.")

    handler = (handlers or {}).get(proposal.tool_name)
    if handler is None:
        return decision, ToolExecutionResult(proposal_id=proposal.proposal_id, decision_id=decision.decision_id,
                                             executed=False, success=False, error_type="NoHandler",
                                             error_message=f"No implementation registered for {proposal.tool_name}.")
    try:
        data = handler(proposal.arguments or {}, context)
        return decision, ToolExecutionResult(proposal_id=proposal.proposal_id, decision_id=decision.decision_id,
                                             executed=True, success=True, result_data=data)
    except Exception as exc:
        return decision, ToolExecutionResult(proposal_id=proposal.proposal_id, decision_id=decision.decision_id,
                                             executed=True, success=False, error_type=type(exc).__name__,
                                             error_message=str(exc)[:500])
