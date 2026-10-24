"""Predict the likely failure category for a traced run with the promoted model."""

from __future__ import annotations

import uuid
from functools import lru_cache
from typing import Any

import joblib

from bifura.learning.dataset import HEALTHY
from bifura.learning.train import MODELS, load_registry, rules_baseline
from bifura.schemas.models import PredictionResult


@lru_cache(maxsize=4)
def _load(version: str):
    return joblib.load(MODELS / f"{version}.joblib")


def current_model() -> tuple[str | None, str | None]:
    reg = load_registry()
    version = reg.get("promoted")
    dataset = next((m["dataset_version"] for m in reg["models"] if m["model_version"] == version), None)
    return version, dataset


def predict_failure(run_id: str, features: dict[str, Any], incident_ids: list[str] | None = None) -> PredictionResult:
    """Ranked categories from the promoted model, or the rules baseline if none is trained."""
    version, dataset = current_model()
    pid = f"pred-{uuid.uuid4().hex[:8]}"
    if version is None:
        cat = rules_baseline(features["text"])
        return PredictionResult(run_id=run_id, prediction_id=pid, model_version="rules-baseline",
                                dataset_version="none", prediction_mode="rules_baseline",
                                predicted_categories=[cat], candidates=[{"category": cat, "score": 1.0, "score_kind": "rule_match"}],
                                scores={cat: 1.0}, score_meaning="rule_match_not_a_probability",
                                supporting_incident_ids=incident_ids or [])
    model = _load(version)
    proba = model.predict_proba([features["text"]])[0]
    ranked = sorted(zip(model.classes_, proba), key=lambda kv: -kv[1])
    cands = [{"category": c, "score": round(float(s), 3), "score_kind": "model_score_uncalibrated"} for c, s in ranked[:4]]
    top = ranked[0][0]
    return PredictionResult(
        run_id=run_id, prediction_id=pid, model_version=version, dataset_version=dataset or "unknown",
        prediction_mode="trained_classifier", predicted_categories=[c["category"] for c in cands[:2]],
        candidates=cands, scores={c["category"]: c["score"] for c in cands},
        score_meaning="model_score_uncalibrated", abstained=top == HEALTHY,
        abstention_reason="The model sees no failure pattern in this trace." if top == HEALTHY else None,
        supporting_incident_ids=incident_ids or [])
