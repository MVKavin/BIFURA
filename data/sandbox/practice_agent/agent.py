"""Revenue research agent: Bifura's practice agent under test.

Task: report a company's year-over-year revenue growth.
Plan: fetch the investor page, extract revenue, calculate growth, write the report.

This is the clean version. Bifura copies it into data/sandbox/runtime/<run_id>/,
injects a known fault for a scenario, runs it with the instrumentation SDK, and
then investigates and patches only that disposable copy.
"""

from bifura.sdk import Tracer

MAX_RETRIES = 2
PLAN = ["fetch_page", "extract_revenue", "calc_growth", "write_report"]
PAGES: dict[str, str] = {}


class TransientError(Exception):
    """A temporary failure that is worth retrying, such as HTTP 503."""


def fetch_page(url):
    page = PAGES.get(url)
    if page is None or page == "__404__":
        raise LookupError(f"404 not found: {url}")
    if page == "__RESET__":
        raise ConnectionResetError(f"connection reset by {url}")
    if page == "__TIMEOUT__":
        raise TimeoutError(f"timed out fetching {url}")
    if page == "__503__":
        raise TransientError(f"503 service unavailable: {url}")
    return page


def extract_revenue(page):
    row = next(line for line in page.splitlines() if line.startswith("Revenue"))
    txt = row.split("=")[1].split("(")[0].strip()  # e.g. "12,400"
    value = int(txt.replace(",", ""))
    return value


def calc_growth(current, previous):
    return round((current - previous) / previous * 100, 1)


def write_report(company, growth):
    if growth is None:
        return f"{company} revenue growth: not available."
    direction = "grew" if growth >= 0 else "fell"
    return f"{company} revenue {direction} {abs(growth)}%."


def fetch_with_retry(t, url, deps):
    for attempt in range(1, MAX_RETRIES + 2):
        try:
            return t.tool("fetch_page", fetch_page, {"url": url}, deps=deps,
                          kind="tool call", summarize=lambda p: p.splitlines()[0][:40])
        except TransientError:
            if attempt > MAX_RETRIES:
                raise


def run(env, t: Tracer):
    """Run the task described by ``env`` and return the final agent state."""
    PAGES.clear()
    PAGES.update(env["pages"])
    company = env["company"]
    task = t.task(env["task"], env.get("expected_text"))
    plan_ev = t.decision("Plan", {"plan": list(PLAN)}, deps=[task], summary=" · ".join(PLAN))
    state = {"page": None, "revenue": None, "prev_revenue": env["prev_revenue"], "growth": None, "report": None}
    src = {"prev_revenue": task}

    for step in PLAN:
        if step == "fetch_page":
            state["page"], src["page"] = fetch_with_retry(t, env["url"], deps=[plan_ev])
        elif step == "extract_revenue":
            value, ev = t.tool("extract_revenue", extract_revenue, {"page": state["page"]},
                               deps=[src.get("page")], kind="decision",
                               summarize=lambda v: f"revenue = {v}")
            state["revenue"] = value
            src["revenue"] = t.state({"revenue": state["revenue"]}, deps=[ev])
        elif step == "calc_growth":
            args = {"current": state["revenue"], "previous": state["prev_revenue"]}
            growth, ev = t.tool("calc_growth", calc_growth, args,
                                deps=[src.get("revenue"), src["prev_revenue"]], kind="tool call",
                                summarize=lambda g: f"growth {g:+}%")
            state["growth"] = growth
            src["growth"] = t.state({"growth": state["growth"]}, deps=[ev])
        elif step == "write_report":
            report, ev = t.tool("write_report", write_report, {"company": company, "growth": state["growth"]},
                                deps=[src.get("growth"), plan_ev], kind="tool call",
                                summarize=lambda r: r[:40])
            state["report"] = report
            src["report"] = ev

    final = t.finish({"report": state["report"]}, deps=[src.get("report")])
    growth = state["growth"]
    t.check("Growth in range", growth is not None and -50 <= growth <= 80,
            f"growth = {growth}", deps=[final, src.get("growth")], rule="growth must be between -50% and +80%")
    return state
