"""Tests for the dashboard loader payload and the embedded investigation UI."""

import json
import re
from pathlib import Path

from bifura.dashboard import format_bundle_for_ui, get_dashboard_html, load_run_bundle
from bifura.dashboard.viewer import DATA_PLACEHOLDER, TEMPLATE_PATH

R0412 = Path("data/fixtures/r0412_revenue_growth.json")
MOCK = Path("data/fixtures/mock_run_bundle.json")


def _payload(path: Path) -> dict:
    return format_bundle_for_ui(load_run_bundle(path))


def _embedded_data(html: str) -> dict:
    match = re.search(r"const DATA=(\{.*?\});\n", html, re.S)
    assert match, "run data was not embedded"
    return json.loads(match.group(1).replace("<\\/", "</"))


def test_r0412_payload_matches_ui_shape():
    p = _payload(R0412)
    assert p["status"] == "failed"  # enum value, not "RunStatus.FAILED"
    assert p["run_id"] == "R-0412"
    ids = [n["id"] for n in p["nodes"]]
    assert ids == [f"n{i}" for i in range(1, 11)]
    for n in p["nodes"]:
        assert {"i", "id", "tag", "l", "sub", "x", "y", "in", "o", "st"} <= n.keys()
    node_ids = set(ids)
    for e in p["edges"]:
        assert e["s"] in node_ids and e["t"] in node_ids
    inferred = {(e["s"], e["t"]) for e in p["edges"] if e["inf"]}
    assert inferred == {("n7", "n8"), ("n10", "n5")}
    assert p["deviation"]["first_deviation_event_id"] == "n5"
    assert p["raw_events"]["n5"]["event_id"] == "n5"
    assert p["narrative"] and "nodes" in p["narrative"]


def test_graph_is_synthesized_from_dependencies_when_missing():
    data = json.loads(R0412.read_text(encoding="utf-8"))
    data["impact_graph"] = None
    p = format_bundle_for_ui(load_run_bundle(data))
    assert p["nodes"][0]["id"] == "task"
    assert ("n4", "n5") in {(e["s"], e["t"]) for e in p["edges"]}


def test_mock_bundle_without_layout_still_renders():
    p = _payload(MOCK)
    assert p["narrative"] is None
    xs = [n["x"] for n in p["nodes"]]
    assert len(set(xs)) == len(xs), "nodes without positions must not overlap"


def test_dashboard_html_embeds_runs_safely():
    p = _payload(R0412)
    p["task_text"] = "</script><script>alert(1)</script>"
    html = get_dashboard_html([p], active_run_id="R-0412")
    assert DATA_PLACEHOLDER not in html
    assert "</script><script>alert(1)" not in html
    data = _embedded_data(html)
    assert data["active"] == "R-0412"
    assert data["runs"][0]["task_text"] == p["task_text"]


def test_template_keeps_the_design_theme():
    css = TEMPLATE_PATH.read_text(encoding="utf-8")
    for token in ("--bg:#0d0d0e", "--acc:#ff6b3d", "--sage:#8fd1a6", "--blue:#7f9cf0", "Geist"):
        assert token in css
