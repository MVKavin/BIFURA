"""Learning/prediction tests: no leakage, honest splits, working predictions."""

import pytest

import bifura.learning.predict as predict
from bifura.learning.dataset import HEALTHY, run_case
from bifura.learning.train import rules_baseline, split_by_family
from bifura.schemas.models import PredictionResult
from bifura.tracing.runner import load_faults, load_scenarios


@pytest.fixture
def env():
    return load_scenarios()["revenue_separator"]["env"]


def test_features_do_not_leak_the_fault_label(env, tmp_path):
    faults = load_faults()
    rec = run_case(faults["sep_decimal"], env, "L-1", tmp_path)
    assert rec is not None
    text = rec["text"]
    assert "sep_decimal" not in text and "state_or_dataflow" not in text
    assert "dev_in_tool_output" in text and "ratio_div_10_1000" in text


def test_healthy_run_has_no_deviation(env, tmp_path):
    rec = run_case(None, env, "L-2", tmp_path)
    assert rec is not None and "no_deviation" in rec["text"]
    assert rules_baseline(rec["text"]) == HEALTHY


def test_family_split_never_shares_a_fault_family():
    records = [{"family": f"{c}-{k}", "label": c, "data_origin": "synthetic_fault_injection", "text": ""}
               for c in ("a", "b") for k in range(3) for _ in range(4)]
    records += [{"family": HEALTHY, "label": HEALTHY, "data_origin": "synthetic_fault_injection", "text": ""}] * 20
    train, test = split_by_family(records)
    fam = lambda rs: {r["family"] for r in rs if r["label"] != HEALTHY}
    assert fam(train) and fam(test) and not fam(train) & fam(test)


def test_prediction_falls_back_to_rules_without_a_model(monkeypatch):
    monkeypatch.setattr(predict, "current_model", lambda: (None, None))
    p = predict.predict_failure("R-x", {"text": "dev_in_plan plan_reordered"})
    assert isinstance(p, PredictionResult)
    assert p.prediction_mode == "rules_baseline" and p.predicted_categories == ["planning_or_tool_sequence"]


def test_trained_model_prediction_is_labelled_uncalibrated(env, tmp_path):
    if predict.current_model()[0] is None:
        pytest.skip("no trained model in models/")
    rec = run_case(load_faults()["swapped_args"], env, "L-3", tmp_path)
    p = predict.predict_failure("R-y", rec)
    assert p.score_meaning == "model_score_uncalibrated"
    assert p.candidates[0]["category"] == "tool_input_validation"
