"""Incident memory: structured incident records plus their trace features.

Each incident is ``data/incidents/<id>.json`` (an IncidentRecord) with a sidecar
``<id>.features.json`` used for retrieval and, once approved, for training.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from bifura.learning.dataset import HEALTHY, load_dataset
from bifura.learning.train import split_by_family
from bifura.schemas.models import FailureCategory, IncidentRecord, LabelStatus
from bifura.tracing.runner import DATA_DIR, load_faults

INCIDENTS = DATA_DIR / "incidents"


def save_incident(record: IncidentRecord, features: dict[str, Any]) -> None:
    INCIDENTS.mkdir(parents=True, exist_ok=True)
    (INCIDENTS / f"{record.incident_id}.json").write_text(record.model_dump_json(indent=2), encoding="utf-8")
    (INCIDENTS / f"{record.incident_id}.features.json").write_text(json.dumps(features, ensure_ascii=False), encoding="utf-8")


def list_incidents() -> list[tuple[IncidentRecord, dict[str, Any]]]:
    out = []
    for path in sorted(INCIDENTS.glob("*.json")):
        if path.name.endswith(".features.json"):
            continue
        rec = IncidentRecord.model_validate_json(path.read_text(encoding="utf-8"))
        fpath = INCIDENTS / f"{rec.incident_id}.features.json"
        feats = json.loads(fpath.read_text(encoding="utf-8")) if fpath.exists() else {"text": ""}
        out.append((rec, feats))
    return out


def get_incident(incident_id: str) -> IncidentRecord | None:
    path = INCIDENTS / f"{incident_id}.json"
    return IncidentRecord.model_validate_json(path.read_text(encoding="utf-8")) if path.exists() else None


def approve_incident(incident_id: str, reviewer: str = "human reviewer") -> IncidentRecord:
    """Human review: make a verified incident eligible for the next training dataset."""
    rec = get_incident(incident_id)
    if rec is None:
        raise KeyError(incident_id)
    if rec.label_status != LabelStatus.VERIFIED:
        raise ValueError("Only incidents whose fix was verified by replay can be approved for training.")
    feats = json.loads((INCIDENTS / f"{incident_id}.features.json").read_text(encoding="utf-8"))
    rec = rec.model_copy(update={"training_eligible": True, "training_eligibility": "approved",
                                 "review_status": f"approved by {reviewer}",
                                 "reviewed_at": datetime.now(timezone.utc)})
    save_incident(rec, feats)
    return rec


def seed_from_dataset(dataset_version: str) -> int:
    """Seed incident memory with one ground-truth incident per training fault family.

    Only training-split records are used, so held-out evaluation families never
    leak into retrieval.
    """
    records = load_dataset(dataset_version)
    train, _ = split_by_family(records)
    faults = load_faults()
    seen, n = set(), 0
    for r in train:
        fam = r["family"]
        if fam in seen or r["label"] == HEALTHY or r["data_origin"] != "synthetic_fault_injection":
            continue
        seen.add(fam)
        n += 1
        title = faults.get(fam, {}).get("title", fam)
        rec = IncidentRecord(
            incident_id=f"INC-S{n:03d}", task_summary="Revenue growth report (practice agent)",
            observed_pattern=title, first_deviation_event_id=r.get("first_deviation_event_id"),
            failure_category=FailureCategory(r["label"]), label_status=LabelStatus.VERIFIED,
            root_cause_status="verified", root_cause_summary=title, verified_root_cause=title,
            verified_correction="Injected fault removed (ground truth by construction)",
            replay_status="passed", data_origin="synthetic_fault_injection", provenance="synthetic_fault_injection",
            training_eligible=True, training_eligibility="approved", review_status="approved (synthetic seed)",
            dataset_version=dataset_version)
        save_incident(rec, {"text": r["text"], "family": fam})
    return n


def approved_live_records() -> list[dict[str, Any]]:
    """Approved, verified incidents from live investigations, as dataset records."""
    out = []
    for rec, feats in list_incidents():
        if rec.data_origin == "real_local_run" and rec.training_eligible and rec.label_status == LabelStatus.VERIFIED:
            out.append({"record_id": rec.incident_id, "family": f"live:{feats.get('family', rec.incident_id)}",
                        "label": rec.failure_category.value, "data_origin": "real_local_run", "text": feats["text"]})
    return out
