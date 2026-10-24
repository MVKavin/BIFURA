"""Bifura instrumentation SDK.

An agent under test imports this and wraps its steps; every step is captured as a
canonical ``TraceEvent`` while the agent runs, so no trace has to be exported by hand.

    from bifura.sdk import Tracer
    t = Tracer(run_id="R-1")
    task = t.task("Report growth")
    page, ev = t.tool("fetch_page", fetch_page, {"url": url}, deps=[task])
"""

from bifura.sdk.tracer import Tracer

__all__ = ["Tracer"]
