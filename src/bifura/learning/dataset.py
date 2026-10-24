"""Build the labelled training dataset by running the practice agent with injected faults.

Every record comes from a real traced run of data/sandbox/practice_agent/agent.py.
Labels are the injected fault's category (ground truth by construction), and all
records are marked ``synthetic_fault_injection``. Approved incidents from live
investigations are appended as ``real_local_run`` in later dataset versions.
"""

from __future__ import annotations

import json
import random
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bifura.analysis.deviation import evaluate_expectations, find_first_deviation
from bifura.learning.features import extract_features
from bifura.tracing.runner import DATA_DIR, RUNTIME, apply_fault_env, load_faults, prepare_workspace, run_agent

DATASETS = DATA_DIR / "datasets"
HEALTHY = "healthy"
COMPANIES = ["ACME", "Globex", "Initech", "Umbrella", "Soylent", "Hooli", "Stark", "Wayne", "Tyrell", "Cyberdyne",
             "Wonka", "Gringotts", "Monarch", "Vandelay", "Prestige", "Oscorp", "Aperture", "Massive", "Pied Piper"]


def _random_env(rng: random.Random) -> dict[str, Any]:
    company = rng.choice(COMPANIES)
    slug = company.lower().replace(" ", "")
    prev = rng.randrange(1_200, 90_000)
    growth_target = rng.uniform(-30, 60)
    revenue = max(1_100, int(prev * (1 + growth_target / 100)))
    growth = round((revenue - prev) / prev * 100, 1)
    year = rng.choice([24, 25, 26])
    url = f"{slug}.example/ir/fy{year}"
    unit = rng.choice(["₹ lakh", "₹ crore", "USD k"])
    return {"company": company, "task": f"Report {company}'s year-over-year revenue growth",
            "expected_text": f"Growth of about {growth:+}%", "url": url,
            "pages": {url: f"{company} results\nRevenue FY{year} = {revenue:,} ({unit})"},
            "prev_revenue": prev, "cached_revenue": int(prev * rng.uniform(0.9, 1.1)),
            "expected": {"revenue": revenue, "prev_revenue": prev, "growth": growth}}


def run_case(fault: dict[str, Any] | None, env: dict[str, Any], run_id: str, root: Path) -> dict[str, Any] | None:
    """Run one case and return its feature record, or None if the fault did not manifest."""
    env = apply_fault_env(env, fault)
    ws = prepare_workspace(run_id, fault, env, root=root)
    run = evaluate_expectations(run_agent(ws, env, run_id), env)
    deviation = find_first_deviation(run, env)
    if fault is not None and not deviation.found:
        return None  # the injected bug did not change behaviour on these inputs
    if fault is None and deviation.found:
        return None
    feats = extract_features(run.events, deviation)
    return {**feats, "first_deviation_event_id": deviation.first_deviation_event_id}


def build_dataset(version: str | None = None, per_family: int = 14, healthy: int = 40, seed: int = 7,
                  extra_records: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Generate ``data/datasets/<version>.jsonl`` and its manifest. Returns the manifest."""
    rng = random.Random(seed)
    version = version or next_version()
    work = RUNTIME / f"_dataset_{version}"
    records, skipped = [], 0
    try:
        families = [(f, f["id"], f["category"]) for f in load_faults().values()] + [(None, HEALTHY, HEALTHY)]
        for fault, family, category in families:
            n = healthy if fault is None else per_family
            for i in range(n):
                rec = run_case(fault, _random_env(rng), f"{family}-{i:03d}", work)
                if rec is None:
                    skipped += 1
                    continue
                records.append({"record_id": f"{version}-{family}-{i:03d}", "family": family, "label": category,
                                "data_origin": "synthetic_fault_injection", **rec})
    finally:
        shutil.rmtree(work, ignore_errors=True)
    records += extra_records or []

    DATASETS.mkdir(parents=True, exist_ok=True)
    path = DATASETS / f"{version}.jsonl"
    with path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    counts: dict[str, int] = {}
    for r in records:
        counts[r["label"]] = counts.get(r["label"], 0) + 1
    manifest = {"dataset_version": version, "created_at": datetime.now(timezone.utc).isoformat(),
                "records": len(records), "skipped_no_effect": skipped, "label_counts": counts,
                "families": sorted({r["family"] for r in records}), "seed": seed,
                "origins": sorted({r["data_origin"] for r in records}),
                "note": "Synthetic fault-injection traces from the practice agent; labels are injected ground truth."}
    (DATASETS / f"{version}.manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def list_versions() -> list[str]:
    return sorted(p.name.removesuffix(".manifest.json") for p in DATASETS.glob("*.manifest.json"))


def next_version() -> str:
    nums = [int(v.split("-v")[-1]) for v in list_versions() if v.startswith("dataset-v")]
    return f"dataset-v{max(nums, default=0) + 1}"


def load_dataset(version: str) -> list[dict[str, Any]]:
    path = DATASETS / f"{version}.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
