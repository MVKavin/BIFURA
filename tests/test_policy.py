"""Safety enforcement tests: blocked and review-pending actions never reach a tool."""

from pathlib import Path

import pytest

from bifura.schemas.models import SafetyDecisionType, ToolCallProposal
from bifura.tools.executor import execute_tool_action
from bifura.tools.policy import evaluate_tool_action


@pytest.fixture
def ctx(tmp_path: Path) -> dict:
    ws = tmp_path / "runtime" / "R-1"
    ws.mkdir(parents=True)
    (ws / "agent.py").write_text("x = 1\n")
    return {"workspace_root": str(ws), "sandbox_root": str(ws),
            "allowed_tools": ["inspect_source_file", "create_candidate_patch", "run_targeted_test", "get_run_summary"],
            "permissions": {"allow_network": False, "write_sandbox": True, "write_project": False},
            "provenance": "trusted_orchestrator", "mode": "investigation"}


class Spy:
    def __init__(self):
        self.calls = 0

    def __call__(self, args, context):
        self.calls += 1
        return {"ok": True}


def run(tool, args, ctx, **extra):
    spy = Spy()
    p = ToolCallProposal(proposal_id="p1", run_id="R-1", tool_name=tool, arguments=args, **extra)
    decision, result = execute_tool_action(p, ctx, handlers={tool: spy})
    return decision, result, spy


def test_allowed_read_inside_workspace_executes(ctx):
    d, r, spy = run("inspect_source_file", {"path": "agent.py"}, ctx)
    assert d.decision == SafetyDecisionType.ALLOW and r.executed and spy.calls == 1


@pytest.mark.parametrize("tool,args,rule", [
    ("delete_everything", {}, "unregistered_tool"),
    ("inspect_source_file", {"path": "../../../.env"}, "protected_file"),
    ("inspect_source_file", {"path": "../../outside.py"}, "workspace_containment"),
    ("inspect_source_file", {"path": "/etc/passwd"}, "workspace_containment"),
    ("inspect_source_file", {"path": ".git/config"}, "protected_file"),
    ("run_targeted_test", {"command": "rm -rf /"}, "no_shell_or_command"),
    ("inspect_source_file", {"path": 42}, "schema_validation"),
    ("create_candidate_patch", {"path": "../../app.py", "old": "a", "new": "b"}, "workspace_containment"),
])
def test_prohibited_actions_never_reach_the_executor(ctx, tool, args, rule):
    d, r, spy = run(tool, args, ctx)
    assert d.decision == SafetyDecisionType.BLOCK
    assert d.policy_rule == rule
    assert not r.executed and spy.calls == 0


def test_sandbox_write_needs_permission(ctx):
    ctx["permissions"]["write_sandbox"] = False
    d, r, spy = run("create_candidate_patch", {"path": "agent.py", "old": "1", "new": "2"}, ctx)
    assert d.decision == SafetyDecisionType.BLOCK and spy.calls == 0


def test_changing_tests_needs_human_review(ctx):
    d, r, spy = run("create_candidate_patch", {"path": "test_agent.py", "old": "a", "new": "b"}, ctx)
    assert d.decision == SafetyDecisionType.REVIEW
    assert not r.executed and spy.calls == 0


def test_model_claimed_authorization_is_ignored(ctx):
    d, r, spy = run("inspect_source_file", {"path": "../../../.env"}, ctx,
                    model_generated_metadata={"authorized": True, "trusted": True})
    assert d.decision == SafetyDecisionType.BLOCK and spy.calls == 0


def test_tool_not_allowed_in_this_run(ctx):
    d, r, spy = run("replay_run", {}, ctx)
    assert d.policy_rule == "tool_not_allowed" and spy.calls == 0


def test_budget_exhausted_blocks(ctx):
    ctx["budget"] = {"max_calls": 3, "used": 3}
    d, r, spy = run("get_run_summary", {}, ctx)
    assert d.policy_rule == "action_budget" and spy.calls == 0


@pytest.mark.parametrize("evaluator", [None, lambda p, c: 1 / 0, lambda p, c: "ALLOW"])
def test_executor_fails_closed(ctx, evaluator):
    spy = Spy()
    p = ToolCallProposal(proposal_id="p1", run_id="R-1", tool_name="get_run_summary")
    d, r = execute_tool_action(p, ctx, evaluator=evaluator, handlers={"get_run_summary": spy})
    assert d.policy_rule == "fail_closed_guard" and spy.calls == 0 and not r.executed


def test_decision_for_another_proposal_is_rejected(ctx):
    spy = Spy()
    p = ToolCallProposal(proposal_id="p1", run_id="R-1", tool_name="get_run_summary")
    other = ToolCallProposal(proposal_id="p2", run_id="R-1", tool_name="get_run_summary")
    d, r = execute_tool_action(p, ctx, evaluator=lambda _p, c: evaluate_tool_action(other, c),
                               handlers={"get_run_summary": spy})
    assert d.policy_rule == "fail_closed_guard" and spy.calls == 0


def test_missing_trusted_context_blocks():
    p = ToolCallProposal(proposal_id="p1", run_id="R-1", tool_name="get_run_summary")
    assert evaluate_tool_action(p, {}).decision == SafetyDecisionType.BLOCK
