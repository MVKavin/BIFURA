"""Build the causal-impact graph from recorded event dependencies (NetworkX)."""

from __future__ import annotations

import json
from typing import Any

import networkx as nx

from bifura.schemas.models import DependencyEdge, EventStatus, EvidenceStatus, ImpactGraph, TraceEvent

_ROW = {"tool call": 170, "assertion": 425, "code": 545}


def _short(value: Any, n: int = 80) -> str:
    if value in (None, {}, []):
        return "—"
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return text if len(text) <= n else text[: n - 1] + "…"


def _tag(e: TraceEvent) -> str:
    kind = e.metadata.get("kind")
    if kind:
        return kind
    return "tool call" if e.tool_name else "event"


def _edge_type(src: TraceEvent, dst: TraceEvent) -> str:
    dt = _tag(dst)
    if dt == "assertion":
        return "validates"
    if dt == "state":
        return "updates"
    if src.name == "Plan":
        return "invokes"
    if dt == "output":
        return "returns"
    return "consumes"


def to_networkx(events: list[TraceEvent]) -> nx.DiGraph:
    g = nx.DiGraph()
    ids = {e.event_id for e in events}
    for e in events:
        g.add_node(e.event_id, event=e)
    for e in events:
        for dep in e.data_dependencies:
            if dep in ids:
                g.add_edge(dep, e.event_id)
    return g


def downstream_of(events: list[TraceEvent], event_id: str | None) -> list[str]:
    """Events that (transitively) consumed data from ``event_id``, in trace order."""
    if not event_id:
        return []
    g = to_networkx(events)
    if event_id not in g:
        return []
    order = {e.event_id: e.sequence for e in events}
    return sorted(nx.descendants(g, event_id), key=order.get)


def build_impact_graph(run_id: str, events: list[TraceEvent], deviation_event_id: str | None = None,
                       suspect: dict[str, Any] | None = None) -> ImpactGraph:
    """Lay out trace events as dashboard nodes; edges come only from recorded dependencies.

    ``suspect`` (from the investigation) adds a source-code node with an *inferred*
    ``suspected cause`` edge to the deviation, which stays dashed until verified.
    """
    by_id = {e.event_id: e for e in events}
    nodes: list[dict[str, Any]] = []
    col, x_of = -1, {}
    prev_tool_col = None
    assertions = []
    for e in events:
        tag = _tag(e)
        if tag == "assertion":
            assertions.append(e)
            continue
        if tag == "state" and prev_tool_col is not None:
            c = prev_tool_col
            prev_tool_col = None
        else:
            col += 1
            c = col
            prev_tool_col = c if tag == "tool call" else None
        x_of[e.event_id] = c
        nodes.append(_node(e, tag, 70 + c * 135, _ROW.get(tag, 295)))
    for k, e in enumerate(assertions):
        anchor = max((x_of.get(d, 0) for d in e.data_dependencies), default=col)
        c = min(anchor, col) - (len(assertions) - 1 - k)
        nodes.append(_node(e, "assertion", 70 + max(c, 0) * 135, 425))

    edges: list[DependencyEdge] = []
    for e in events:
        for dep in e.data_dependencies:
            if dep in by_id:
                edges.append(DependencyEdge(
                    from_event_id=dep, to_event_id=e.event_id, run_id=run_id,
                    dependency_type=_edge_type(by_id[dep], e), evidence_status=EvidenceStatus.OBSERVED,
                    evidence_refs=[dep, e.event_id],
                    explanation=f"Recorded in the trace: {e.name} declared {by_id[dep].name} (#{by_id[dep].sequence}) as an input."))

    if suspect and deviation_event_id in by_id:
        dev_x = 70 + x_of.get(deviation_event_id, 0) * 135
        nodes.append({"id": "src", "tag": "code", "label": suspect["label"], "sub": suspect.get("sub", "suspected location"),
                      "x": dev_x, "y": _ROW["code"], "in": "—", "o": suspect.get("detail", "—"),
                      "st": suspect.get("status", "hypothesis")})
        edges.append(DependencyEdge(
            from_event_id="src", to_event_id=deviation_event_id, run_id=run_id,
            dependency_type="suspected cause", evidence_status=EvidenceStatus.INFERRED,
            explanation=suspect.get("why", "Investigation hypothesis; unverified until replay passes.")))
    return ImpactGraph(run_id=run_id, nodes=nodes, edges=edges,
                       evidence_refs=[deviation_event_id] if deviation_event_id else [])


def _node(e: TraceEvent, tag: str, x: float, y: float) -> dict[str, Any]:
    failed = e.status == EventStatus.FAILURE.value or e.event_type == "error"
    return {"id": e.event_id, "tag": tag, "label": e.name or e.tool_name or e.event_type,
            "sub": _short(e.summary, 40), "x": x, "y": y,
            "in": _short(e.input_data), "o": _short(e.output_data if not e.error else f"{e.error_type}: {e.error}"),
            "st": _short(e.state_delta) if e.state_delta else ("failed" if failed else "—")}
