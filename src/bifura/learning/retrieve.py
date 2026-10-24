"""Retrieve similar past incidents (explainable similarity; this is not training)."""

from __future__ import annotations

import uuid
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from bifura.learning.incident_store import list_incidents
from bifura.schemas.models import IncidentMatch, LabelStatus

_INFORMATIVE = ("dev_", "err", "plan_", "ratio_", "fail_", "run_unfinished")


def retrieve_similar(run_id: str, features: dict[str, Any], k: int = 3,
                     exclude: set[str] | None = None) -> list[IncidentMatch]:
    store = [(r, f) for r, f in list_incidents() if f.get("text") and r.incident_id not in (exclude or set())]
    if not store:
        return []
    vec = TfidfVectorizer(token_pattern=r"[^ ]+", lowercase=False, sublinear_tf=True)
    mat = vec.fit_transform([f["text"] for _, f in store] + [features["text"]])
    sims = cosine_similarity(mat[-1], mat[:-1])[0]
    mine = {t for t in features["text"].split() if t.startswith(_INFORMATIVE)}
    out = []
    for idx in sims.argsort()[::-1][:k]:
        rec, feats = store[idx]
        shared = sorted(mine & {t for t in feats["text"].split() if t.startswith(_INFORMATIVE)})
        verified = rec.label_status == LabelStatus.VERIFIED
        out.append(IncidentMatch(
            incident_id=rec.incident_id, match_id=f"match-{uuid.uuid4().hex[:8]}", run_id=run_id,
            similarity_score=round(float(max(0.0, min(1.0, sims[idx]))), 3),
            match_reason=f"{rec.root_cause_summary or rec.observed_pattern} ({rec.failure_category.value})",
            why_relevant=f"{'Verified' if verified else 'Provisional'} incident, {rec.data_origin.replace('_', ' ')}; "
                         f"shares {len(shared)} trace signals.",
            matched_features=shared[:6], verified=verified))
    return out
