"""Bifura dashboard package.

Provides loader and viewer components to render the fluid interactive investigation
interface for Streamlit and standalone browsers.
"""

from bifura.dashboard.loader import load_run_bundle, load_all_bundles, format_bundle_for_ui
from bifura.dashboard.viewer import render_dashboard, get_dashboard_html

__all__ = [
    "load_run_bundle",
    "load_all_bundles",
    "format_bundle_for_ui",
    "render_dashboard",
    "get_dashboard_html",
]
