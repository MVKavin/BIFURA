"""Train, evaluate and register the failure-category model (TF-IDF + Logistic Regression).

Evaluation holds out whole fault *families* (one per category), so the reported
score measures generalisation to bug variants the model never saw, not memorised
duplicates. The model is compared with a majority-class baseline and a hand-written
rules baseline; it is promoted only if it beats the majority baseline.
"""

from __future__ import annotations

import json
import random
from datetime import datetime, timezone
from typing import Any

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_recall_fscore_support
from sklearn.pipeline import Pipeline

from bifura.learning.dataset import HEALTHY, load_dataset
from bifura.tracing.runner import REPO_ROOT

MODELS = REPO_ROOT / "models"
RESULTS = REPO_ROOT / "results" / "evaluation"
REGISTRY = MODELS / "registry.json"


def rules_baseline(text: str) -> str:
    """Expert rules over the same tokens, written by the team.

    The authors knew every fault family when writing them, so this is a reference
    ceiling rather than a blind baseline. Its value is that it needs no data; the
    model's value is that it is learned and retrained from incidents.
    """
    t = set(text.split())
    if "no_deviation" in t:
        return HEALTHY
    if "dev_in_plan" in t:
        return "planning_or_tool_sequence"
    if "err_repeat_over_budget" in t:
        return "retry_logic"
    if "dev_in_tool_input" in t:
        return "tool_input_validation"
    if "dev_in_error" in t:
        return "external_tool_or_environment"
    return "state_or_dataflow"


def split_by_family(records: list[dict[str, Any]], seed: int = 0) -> tuple[list[dict], list[dict]]:
    """Hold out one whole fault family per category, plus 30% of healthy runs."""
    rng = random.Random(seed)
    by_cat: dict[str, set[str]] = {}
    for r in records:
        if r["data_origin"] == "synthetic_fault_injection" and r["label"] != HEALTHY:
            by_cat.setdefault(r["label"], set()).add(r["family"])
    test_families = {sorted(fams)[-1] for fams in by_cat.values() if len(fams) >= 2}
    train, test = [], []
    for r in records:
        if r["label"] == HEALTHY:
            (test if rng.random() < 0.3 else train).append(r)
        elif r["family"] in test_families:
            test.append(r)
        else:
            train.append(r)
    return train, test


def _metrics(y_true: list[str], y_pred: list[str], labels: list[str]) -> dict[str, Any]:
    p, r, f, s = precision_recall_fscore_support(y_true, y_pred, labels=labels, zero_division=0)
    return {"accuracy": round(accuracy_score(y_true, y_pred), 3),
            "macro_f1": round(f1_score(y_true, y_pred, labels=labels, average="macro", zero_division=0), 3),
            "per_class": {lab: {"precision": round(p[i], 3), "recall": round(r[i], 3), "f1": round(f[i], 3),
                                "support": int(s[i])} for i, lab in enumerate(labels)}}


CONFIGS = [{"binary": True, "C": 1.0}, {"binary": False, "C": 1.0}, {"binary": True, "C": 0.3}]


def make_model(binary: bool = True, C: float = 1.0) -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(token_pattern=r"[^ ]+", sublinear_tf=True, lowercase=False, binary=binary)),
        ("clf", LogisticRegression(max_iter=3000, C=C, class_weight="balanced")),
    ])


def select_config(train: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, float]]:
    """Pick model settings by leave-one-family-out CV on the training split only."""
    groups = [r["family"] if r["label"] != HEALTHY else f"healthy-{i % 4}" for i, r in enumerate(train)]
    scores = {}
    for cfg in CONFIGS:
        fold_scores = []
        for g in sorted(set(groups)):
            fit = [r for r, gg in zip(train, groups) if gg != g]
            hold = [r for r, gg in zip(train, groups) if gg == g]
            if len({r["label"] for r in fit}) < 2:
                continue
            m = make_model(**cfg).fit([r["text"] for r in fit], [r["label"] for r in fit])
            fold_scores.append(accuracy_score([r["label"] for r in hold], m.predict([r["text"] for r in hold])))
        scores[json.dumps(cfg)] = round(sum(fold_scores) / max(1, len(fold_scores)), 3)
    best = max(CONFIGS, key=lambda c: scores[json.dumps(c)])
    return best, scores


def load_registry() -> dict[str, Any]:
    if REGISTRY.exists():
        return json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {"promoted": None, "models": []}


def train_and_evaluate(dataset_version: str) -> dict[str, Any]:
    """Train on the family split, evaluate, save artifact + report, promote if it earns it."""
    records = load_dataset(dataset_version)
    train, test = split_by_family(records)
    labels = sorted({r["label"] for r in records})
    config, cv_scores = select_config(train)
    model = make_model(**config).fit([r["text"] for r in train], [r["label"] for r in train])

    y_true = [r["label"] for r in test]
    texts = [r["text"] for r in test]
    y_model = list(model.predict(texts))
    proba = model.predict_proba(texts)
    classes = list(model.classes_)
    top2 = sum(t in [classes[j] for j in row.argsort()[::-1][:2]] for t, row in zip(y_true, proba)) / max(1, len(y_true))
    majority = max(set(r["label"] for r in train), key=[r["label"] for r in train].count)

    registry = load_registry()
    version = f"model-v{len(registry['models']) + 1}"
    report = {
        "model_version": version, "dataset_version": dataset_version,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "algorithm": "TF-IDF over trace tokens + LogisticRegression(class_weight=balanced)",
        "selected_config": config,
        "selection": "leave-one-family-out CV accuracy on the training split only (test labels unseen)",
        "cv_scores": cv_scores,
        "split": "held-out fault families (one per category) + 30% of healthy runs",
        "train_size": len(train), "test_size": len(test),
        "test_families": sorted({r["family"] for r in test if r["label"] != HEALTHY}),
        "labels": labels,
        "model": {**_metrics(y_true, y_model, labels), "top2_accuracy": round(top2, 3)},
        "baseline_majority": {**_metrics(y_true, [majority] * len(y_true), labels), "predicts": majority},
        "baseline_rules": _metrics(y_true, [rules_baseline(t) for t in texts], labels),
        "confusion_matrix": {"labels": labels, "matrix": confusion_matrix(y_true, y_model, labels=labels).tolist()},
        "score_meaning": "uncalibrated model score (ranking), not a probability",
        "limitations": "Small synthetic dataset from one practice agent; held-out families are few, so scores are noisy.",
    }
    promoted = report["model"]["macro_f1"] > report["baseline_majority"]["macro_f1"]
    report["promoted"] = promoted
    report["promotion_rule"] = "promote when held-out macro-F1 beats the majority-class baseline"

    MODELS.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODELS / f"{version}.joblib")
    (RESULTS / f"{version}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    registry["models"].append({k: report[k] for k in ("model_version", "dataset_version", "created_at", "promoted")}
                              | {"macro_f1": report["model"]["macro_f1"]})
    if promoted:
        registry["promoted"] = version
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    return report


def load_report(version: str) -> dict[str, Any] | None:
    path = RESULTS / f"{version}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
