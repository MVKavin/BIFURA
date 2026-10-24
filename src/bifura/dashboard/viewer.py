"""Render the Bifura investigation UI from run-bundle payloads.

The UI is a single self-contained HTML page (``templates/investigation.html``).
Run data is injected as JSON, so the same page works inside Streamlit and as a
standalone file opened in a browser.

Export a standalone page::

    python -m bifura.dashboard results/dashboard.html
"""

import json
import sys
from pathlib import Path
from typing import Any, Iterable

TEMPLATE_PATH = Path(__file__).parent / "templates" / "investigation.html"
DATA_PLACEHOLDER = "/*__BIFURA_DATA__*/null"


def _script_safe_json(data: Any) -> str:
    """Serialize to JSON that can sit inside a <script> tag without closing it."""
    return (
        json.dumps(data, ensure_ascii=False, default=str)
        .replace("</", "<\\/")
        .replace("<!--", "<\\!--")
        .replace(" ", "\\u2028")
        .replace(" ", "\\u2029")
    )


def get_dashboard_html(
    payloads: dict[str, Any] | Iterable[dict[str, Any]],
    active_run_id: str | None = None,
    mode: str = "auto",
    autoplay: bool = False,
    embedded: bool = False,
) -> str:
    """Return the full investigation page with the given UI payloads embedded.

    ``payloads`` are outputs of ``format_bundle_for_ui`` (one dict or a list).
    ``active_run_id`` picks the run shown first (run_id or scenario_id);
    by default the first payload is shown.
    ``mode`` is ``"auto"`` (plays straight through) or ``"step"`` (waits for
    Next / → between steps). With ``autoplay`` the investigation starts on load;
    otherwise it waits for the Run button.
    """
    runs = [payloads] if isinstance(payloads, dict) else list(payloads)
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    if DATA_PLACEHOLDER not in template:
        raise RuntimeError(f"Data placeholder missing from {TEMPLATE_PATH}")
    data = {
        "runs": runs,
        "active": active_run_id,
        "mode": "step" if mode == "step" else "auto",
        "autoplay": bool(autoplay),
        "embedded": bool(embedded),
    }
    return template.replace(DATA_PLACEHOLDER, _script_safe_json(data), 1)


def render_dashboard(
    payloads: dict[str, Any] | Iterable[dict[str, Any]],
    active_run_id: str | None = None,
    height: int = 900,
    mode: str = "auto",
    autoplay: bool = False,
    embedded: bool = False,
) -> None:
    """Embed the investigation UI in the current Streamlit page."""
    import streamlit.components.v1 as components

    html = get_dashboard_html(payloads, active_run_id, mode=mode, autoplay=autoplay, embedded=embedded)
    components.html(html, height=height, scrolling=False)


def main(argv: list[str] | None = None) -> int:
    """Write a standalone dashboard page built from data/fixtures and data/runs."""
    from bifura.dashboard.loader import format_bundle_for_ui, load_all_bundles

    args = sys.argv[1:] if argv is None else argv
    out = Path(args[0] if args else "results/dashboard.html")
    payloads = [format_bundle_for_ui(b) for b in load_all_bundles().values()]
    payloads.sort(key=lambda p: p.get("started_at") or "", reverse=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(get_dashboard_html(payloads), encoding="utf-8")
    print(f"Wrote {out} ({len(payloads)} runs)")
    return 0
