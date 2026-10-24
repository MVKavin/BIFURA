"""One call for the learning cycle: dataset -> train -> evaluate -> (promote) -> seed memory.

    python -m bifura.learning.lifecycle
"""

from __future__ import annotations

import json
from typing import Any

from bifura.learning.dataset import build_dataset
from bifura.learning.incident_store import approved_live_records, list_incidents, seed_from_dataset
from bifura.learning.train import train_and_evaluate


def learn(per_family: int = 14, healthy: int = 40) -> dict[str, Any]:
    """Build a new dataset version (including approved live incidents) and train on it."""
    live = approved_live_records()
    manifest = build_dataset(per_family=per_family, healthy=healthy, extra_records=live)
    report = train_and_evaluate(manifest["dataset_version"])
    seeded = 0
    if not any(r.data_origin == "synthetic_fault_injection" for r, _ in list_incidents()):
        seeded = seed_from_dataset(manifest["dataset_version"])
    return {"dataset": manifest, "report": report, "live_records_added": len(live), "incidents_seeded": seeded}


if __name__ == "__main__":
    out = learn()
    r = out["report"]
    print(json.dumps({"dataset": out["dataset"]["dataset_version"], "records": out["dataset"]["records"],
                      "model": r["model_version"], "promoted": r["promoted"],
                      "macro_f1": r["model"]["macro_f1"], "top2": r["model"]["top2_accuracy"],
                      "majority_f1": r["baseline_majority"]["macro_f1"], "rules_f1": r["baseline_rules"]["macro_f1"],
                      "test_families": r["test_families"], "seeded": out["incidents_seeded"]}, indent=2))
