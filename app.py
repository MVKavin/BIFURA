"""Bifura Streamlit dashboard.

Sidebar: run the practice agent and investigate it live (Gemini or scripted),
pick a run to play, see/retrain the prediction model, approve incidents.
Main area: the investigation story + causal-impact graph.
"""

import json
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
try:
    import bifura  # noqa: F401
except ImportError:  # running without `pip install -e .`
    sys.path.insert(0, str(ROOT / "src"))

from bifura.dashboard import format_bundle_for_ui, get_dashboard_html, load_all_bundles, render_dashboard
from bifura.learning.incident_store import approve_incident, list_incidents
from bifura.learning.train import load_registry, load_report
from bifura.llm import llm_status
from bifura.schemas.models import LabelStatus
from bifura.tracing.runner import load_scenarios

st.set_page_config(page_title="Bifura", page_icon=":material/call_split:", layout="wide", initial_sidebar_state="expanded")
st.markdown(
    """
    <style>
      header[data-testid="stHeader"] {display: none !important;}
      footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stToolbarActions"], [data-testid="stDecoration"],
      [data-testid="stAppDeployButton"], [data-testid="stMainMenu"],
      [data-testid="stStatusWidget"], [data-testid="stSkillsNudge"], [data-testid="stSkillsNudgeAnchor"],
      /* Streamlit's own collapse/expand is unreliable with this full-screen layout; we use our own buttons */
      [data-testid="stSidebarCollapseButton"], [data-testid="stExpandSidebarButton"] {display: none !important;}
      .st-key-hidectl button, .st-key-showctl button {background: #18191b; border: 1px solid #3c3d41;
        color: #ecebe7; min-height: 0; padding: 4px 10px; font-size: 13px;}
      .st-key-hidectl button:hover, .st-key-showctl button:hover {border-color: #ff6b3d; color: #ff6b3d;}
      .st-key-showctl {position: fixed !important; top: 10px; left: 10px; z-index: 1000; width: auto !important;}
      /* "Hide controls" stays pinned at the top of the sidebar even after scrolling it */
      [data-testid="stSidebar"] .st-key-hidectl {position: sticky; top: 0; z-index: 20; background: #131314;
        padding: 10px 0 8px; margin-top: -10px;}
      .block-container, [data-testid="stMainBlockContainer"] {padding: 0 !important; max-width: 100% !important;}
      [data-testid="stAppViewContainer"], .stApp {background: #0d0d0e;}
      /* Streamlit fades the page while a button's work runs; keep the dashboard at full brightness */
      [data-stale="true"], .stale-element, [data-testid="stMain"] [data-testid="stElementContainer"] {
        opacity: 1 !important; filter: none !important; transition: none !important;}
      [data-testid="stMain"] [data-testid="stVerticalBlock"] {gap: 0 !important;}
      [data-testid="stMain"] [data-testid="stElementContainer"]:has(style) {display: none;}
      [data-testid="stMain"] iframe {display: block; width: 100%; height: 100vh !important; border: 0;}
      [data-testid="stSidebar"] {background: #131314; border-right: 1px solid #26272a;}
      [data-testid="stSidebar"] h4 {margin: 14px 0 2px; font-size: 13px; color: #8d8b86; font-weight: 500; letter-spacing: .02em;}
      [data-testid="stSidebarUserContent"] {padding-top: 18px;}
      [data-testid="stMetricValue"] {font-size: 22px;}
    </style>
    """,
    unsafe_allow_html=True,
)

ss = st.session_state
ss.setdefault("active", None)
ss.setdefault("autoplay", False)
ss.setdefault("flash", None)
ss.setdefault("controls", True)
ss.setdefault("view_radio", "agent")

# Controls hidden: remove the sidebar so the dashboard uses the full width, and show a small
# floating ☰ button to bring it back. Both elements always exist (only CSS changes), so the
# dashboard iframe is not reloaded and a playing story keeps going.
# Streamlit also collapses the sidebar by itself on smaller windows (its own arrow is hidden here),
# which used to leave no way back. So when controls are on, force the sidebar open.
_ctl_css = ("[data-testid='stSidebar']{display:none !important;}" if not ss.controls
            else ".st-key-showctl{display:none !important;}"
                 "[data-testid='stSidebar']{transform:none !important;margin-left:0 !important;width:300px !important;"
                 "min-width:300px !important;max-width:300px !important;visibility:visible !important;"
                 "transition:none !important;}"
                 "[data-testid='stSidebar'] > div{width:300px !important;}")
st.markdown(f"<style>{_ctl_css}</style>", unsafe_allow_html=True)
if st.button("Controls", key="showctl", icon=":material/menu:", help="Show the Bifura controls sidebar"):
    ss.controls = True
    st.rerun()


@st.cache_data(show_spinner=False)
def load_runs() -> list[dict]:
    bundles = load_all_bundles(ROOT / "data" / "fixtures", ROOT / "data" / "runs")
    runs = [{"payload": format_bundle_for_ui(b), "json": b.model_dump_json(indent=2)} for b in bundles.values()]
    # Live runs first (newest first), then recorded samples.
    runs.sort(key=lambda r: (not r["payload"].get("is_fixture"), r["payload"].get("started_at") or ""), reverse=True)
    return runs


def run_label(p: dict) -> str:
    who = (p.get("investigator") or {}).get("name") or ("sample" if p.get("is_fixture") else "recorded")
    return f"{p['run_id']} · {p.get('task_summary') or p['task_text']} · {who}"


status = llm_status()
scenarios = load_scenarios()

with st.sidebar:
    if st.button("Hide controls", key="hidectl", icon=":material/left_panel_close:"):
        ss.controls = False
        st.rerun()
    st.markdown(
        """<div style="display:flex;align-items:center;gap:10px;margin:6px 0 2px">
             <svg width="26" height="26" viewBox="0 0 20 20" fill="none" stroke="#ff6b3d" stroke-width="1.8"
                  stroke-linecap="round" style="filter:drop-shadow(0 0 6px rgba(255,107,61,.45))">
               <path d="M3 10h6c3 0 3-5 8-5M9 10c3 0 3 5 8 5"/><circle cx="3" cy="10" r="1.3" fill="#ff6b3d"/></svg>
             <span style="font:600 19px/1 system-ui,-apple-system,'Segoe UI',sans-serif;letter-spacing:-.01em;color:#ecebe7">Bifura</span>
             <span style="font:600 10px/1 ui-monospace,Menlo,monospace;letter-spacing:.08em;color:#8d8b86;
                   border:1px solid #3c3d41;border-radius:5px;padding:3px 6px">DEBUGGER</span></div>""",
        unsafe_allow_html=True)
    st.caption("Incident-informed predictive debugging for multi-step AI agents.")
    if status.ready:
        st.success(f"Gemini connected · {status.model or 'model auto-selected'}", icon=":material/check_circle:")
    else:
        st.warning(status.message, icon=":material/warning:")
        with st.expander("How to connect Gemini"):
            st.markdown(
                "1. Get a key at **aistudio.google.com → Get API key**.\n"
                "2. Copy `.env.example` to `.env` in the project folder.\n"
                "3. Set `GEMINI_API_KEY=your_key` (optional: `LLM_MODEL=gemini-2.5-flash`).\n"
                "4. Restart Streamlit.")

    if ss.get("view_radio") not in ("agent", "kvl"):  # the numeric chat option was removed from the menu
        ss.view_radio = "agent"
    view = st.radio("What do you want to check?", ["agent", "kvl"], key="view_radio",
                    format_func=lambda v: {"agent": ":material/smart_toy: ACME agent (bug demo)",
                                           "kvl": ":material/electric_bolt: KVL circuit check"}[v],
                    help="ACME agent: Bifura debugs a small AI program. KVL: check KVL equations from a chat, an AI "
                         "or you.")
    payloads, mode = [], "Auto"
    if view == "chat":
        from bifura.dashboard.chat_page import sidebar_settings
        chat_settings = sidebar_settings()
    elif view == "kvl":
        from bifura.dashboard.kvl_page import sidebar_settings as kvl_sidebar
        kvl_settings = kvl_sidebar()
    else:
        st.markdown("#### 1 · Run a live investigation")
        sid = st.selectbox("Scenario: the bug injected into the practice agent", list(scenarios),
                           format_func=lambda k: scenarios[k]["title"])
        use_llm = st.toggle("Investigate with Gemini", value=status.ready, disabled=not status.ready,
                            help="Off = scripted investigator (no LLM), clearly labelled as scripted.")
        if st.button("Run agent & investigate", type="primary", icon=":material/play_arrow:", use_container_width=True):
            from bifura.pipeline import investigate
            with st.status("Running the agent…", expanded=True) as box:
                try:
                    out = investigate(sid, use_llm=use_llm, progress=box.write)
                    box.update(label="Fix verified ✓" if out["verified"] else "Finished: fix not verified",
                               state="complete" if out["verified"] else "error")
                    load_runs.clear()
                    ss.active, ss.autoplay = out["run_id"], True
                    ss.flash = f"{out['run_id']}: {out['summary']}"
                except Exception as exc:  # show the failure instead of a blank page
                    box.update(label="Investigation failed", state="error")
                    st.exception(exc)
                    st.stop()
            st.rerun()
        if ss.flash:
            st.caption(ss.flash)

        # ACME mode lists ACME agent runs only. A chat check (KVL/numeric) appears here only when it was
        # opened with "Watch it in the story view".
        runs = [r for r in load_runs()
                if not str(r["payload"].get("scenario_id") or "").startswith("chat-")
                or r["payload"]["run_id"] == ss.get("open_chat")]
        payloads = [r["payload"] for r in runs]
        st.markdown("#### 2 · Show a run")
        ids = [p["run_id"] for p in payloads]
        if not ids:
            st.info("No runs yet. Run a live investigation above.")
        else:
            if ss.active not in ids:
                ss.active = ids[0]
            chosen = st.selectbox("Run", ids, index=ids.index(ss.active),
                                  format_func=lambda i: run_label(payloads[ids.index(i)]))
            if chosen != ss.active:
                ss.active, ss.autoplay = chosen, False
            c1, c2 = st.columns([3, 2])
            mode = c1.radio("Playback", ["Auto", "Step"], horizontal=True,
                            help="Step pauses after every step; press → or the › button to continue.")
            ss.autoplay = c2.toggle("Autoplay", value=ss.autoplay)

        st.markdown("#### 3 · Learning & prediction")
        reg = load_registry()
        rep = load_report(reg["promoted"]) if reg.get("promoted") else None
        if rep:
            m1, m2 = st.columns(2)
            m1.metric("Held-out macro-F1", rep["model"]["macro_f1"],
                      f"{rep['model']['macro_f1'] - rep['baseline_majority']['macro_f1']:+.2f} vs majority")
            m2.metric("Top-2 accuracy", rep["model"]["top2_accuracy"])
            st.caption(f"{rep['model_version']} · {rep['dataset_version']} · {rep['train_size']} train / "
                       f"{rep['test_size']} test runs · tested on unseen bug families: {', '.join(rep['test_families'])}")
            with st.expander("Evaluation details"):
                st.write({"algorithm": rep["algorithm"], "selected settings": rep.get("selected_config"),
                          "majority baseline F1": rep["baseline_majority"]["macro_f1"],
                          "expert rules F1 (written knowing all families)": rep["baseline_rules"]["macro_f1"],
                          "score meaning": rep["score_meaning"]})
                st.dataframe({k: v for k, v in rep["model"]["per_class"].items()}, use_container_width=True)
                st.caption("Confusion matrix (rows = true, columns = predicted): " + ", ".join(rep["confusion_matrix"]["labels"]))
                st.dataframe(rep["confusion_matrix"]["matrix"], use_container_width=True)
                st.caption(rep["limitations"])
        else:
            st.info("No model trained yet.")
        if st.button("Retrain on a new dataset version", use_container_width=True,
                     help="Re-runs the agent with every fault family, adds approved live incidents, trains and evaluates."):
            from bifura.learning.lifecycle import learn
            with st.spinner("Generating traces and training… (about 20 s)"):
                out = learn()
            ss.flash = (f"Trained {out['report']['model_version']} on {out['dataset']['dataset_version']} "
                        f"({out['dataset']['records']} runs, {out['live_records_added']} approved live incidents). "
                        f"Macro-F1 {out['report']['model']['macro_f1']}, promoted: {out['report']['promoted']}.")
            load_runs.clear()
            st.rerun()

        st.markdown("#### 4 · Incident memory")
        incidents = list_incidents()
        live = [r for r, _ in incidents if r.data_origin == "real_local_run"]
        st.caption(f"{len(incidents)} incidents · {len(incidents) - len(live)} synthetic seeds · {len(live)} from live runs")
        pending = [r for r in live if r.label_status == LabelStatus.VERIFIED and not r.training_eligible][-4:]
        for r in pending:
            col1, col2 = st.columns([3, 2])
            col1.caption(f"**{r.incident_id}** · {r.failure_category.value}")
            if col2.button("Approve", key=f"ap-{r.incident_id}", help="Allow this verified incident into the next training set"):
                approve_incident(r.incident_id)
                ss.flash = f"{r.incident_id} approved. It joins the dataset the next time you retrain."
                st.rerun()

        active_run = next((r for r in runs if r["payload"]["run_id"] == ss.active), None)
        if active_run:
            st.markdown("#### Details for this run")
            from bifura.dashboard.live import load_transcript
            t = load_transcript(ss.active)
            if t:
                with st.expander("Investigation transcript"):
                    for s in t["steps"]:
                        icon = {"ALLOW": "✅", "BLOCK": "⛔", "REVIEW": "⏸️"}.get(s["decision"], "•")
                        st.markdown(f"{icon} **{s['actor']}** → `{s['action']}` {json.dumps(s['args'])[:80]}")
                        if s.get("thought"):
                            st.caption(s["thought"])
                    st.markdown("**Diagnosis**")
                    st.write(t.get("diagnosis"))
                    if t.get("diff"):
                        st.code(t["diff"], language="diff")
            with st.expander("Safety audit"):
                st.dataframe([{"decision": d["decision"], "rule": d["policy_rule"], "status": d["execution_status"],
                               "reason": d["reason"][:80]} for d in active_run["payload"]["safety_decisions"]],
                             use_container_width=True)
            with st.expander("Raw run bundle (JSON)"):
                st.code(active_run["json"][:20000], language="json")
            st.download_button("Export standalone report (.html)", get_dashboard_html(payloads, ss.active),
                               file_name=f"bifura-{ss.active}.html", mime="text/html", use_container_width=True)

if view in ("chat", "kvl"):
    st.markdown("""<style>
      [data-testid="stMainBlockContainer"], .block-container {padding: 2.2rem 2.5rem 6rem !important; max-width: min(1100px, 100%) !important; box-sizing: border-box;}
      [data-testid="stMain"] [data-testid="stVerticalBlock"] {gap: 0.8rem !important;}
    </style>""", unsafe_allow_html=True)
    if view == "chat":
        from bifura.dashboard.chat_page import main_area
        main_area(chat_settings)
    else:
        from bifura.dashboard.kvl_page import main_area as kvl_main
        kvl_main(kvl_settings)
elif payloads:
    render_dashboard(payloads, active_run_id=ss.active, height=900, mode=mode.lower(), autoplay=ss.autoplay,
                     embedded=True)
else:
    st.title("Bifura")
    st.info("No runs yet. Use **Run agent & investigate** in the sidebar.")
