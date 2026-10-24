"""Targeted and regression tests for the practice agent.

Bifura runs these inside a sandbox copy (data/sandbox/runtime/<run_id>/) before and
after a candidate patch. scenario_env.json in the same folder holds the scenario's
inputs and expected values.
"""

import importlib.util
import json
from pathlib import Path

from bifura.sdk import Tracer

HERE = Path(__file__).parent
_spec = importlib.util.spec_from_file_location("agent_under_test", HERE / "agent.py")
agent = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(agent)
ENV = json.loads((HERE / "scenario_env.json").read_text(encoding="utf-8"))


def test_extract_reads_thousands_separator():
    assert agent.extract_revenue("Revenue FY25 = 12,400 (₹ lakh)") == 12400


def test_extract_reads_plain_number():
    assert agent.extract_revenue("Revenue FY25 = 980 (₹ lakh)") == 980


def test_growth_formula():
    assert agent.calc_growth(12400, 10500) == 18.1
    assert agent.calc_growth(9000, 7500) == 20.0


def test_plan_calculates_before_reporting():
    plan = agent.PLAN
    assert plan.index("calc_growth") < plan.index("write_report")
    assert set(["fetch_page", "extract_revenue", "calc_growth", "write_report"]) <= set(plan)


def test_scenario_end_to_end():
    state = agent.run(ENV, Tracer("test"))
    expected = ENV["expected"]
    assert state["revenue"] == expected["revenue"]
    assert abs(state["growth"] - expected["growth"]) < 0.05
    assert f"{abs(expected['growth'])}%" in state["report"]
