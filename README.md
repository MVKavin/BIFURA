# Bifura

Bifura is a prototype for incident-informed predictive debugging of multi-step AI-agent executions.

It aims to capture execution traces, identify evidence-supported deviations, retrieve relevant incidents, investigate possible causes, propose bounded fixes, and verify outcomes with tests and replay.

Safety enforcement is required implementation scope. Defining safety-decision data contracts alone does not implement enforcement.

## Requirements

- Python 3.11 or newer
- Git

## Windows setup

Run these commands from the repository root in Command Prompt:

```cmd
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Connect the LLM (Gemini)

Copy `.env.example` to `.env` and set `GEMINI_API_KEY` (free key from https://aistudio.google.com).
Without a key, investigations run in a clearly labelled scripted mode.

## Start the application

```cmd
streamlit run app.py
```

In the sidebar, pick a scenario and click **▶ Run agent & investigate**.
Full walkthrough, controls and demo script: `docs/DASHBOARD_GUIDE.md`.

## Run tests

```cmd
python -m pytest -v
```

## How it fits together

| Stage | Module |
|-------|--------|
| Practice agent under test (3 demo bugs, 16 fault families) | `data/sandbox/practice_agent/`, `data/sandbox/faults.json`, `data/sandbox/scenarios.json` |
| Automatic trace capture (instrumentation SDK) | `src/bifura/sdk/` |
| Fault injection + sandbox copies | `src/bifura/tracing/runner.py` |
| Expected-vs-actual, first deviation, impact graph | `src/bifura/analysis/` |
| Safety gate (ALLOW / REVIEW / BLOCK) + central executor | `src/bifura/tools/` |
| Dataset, features, training, prediction, incident memory, retrieval | `src/bifura/learning/` |
| Gemini adapter (configurable) | `src/bifura/llm/` |
| LangGraph investigation workflow | `src/bifura/agent/` |
| Tests + replay verification | `src/bifura/repair/` |
| End-to-end run | `src/bifura/pipeline.py` |
| Dashboard | `app.py`, `src/bifura/dashboard/` |

## Current implementation status (verified by `python -m pytest`)

- Shared Pydantic contracts: implemented
- Agent tracing (SDK) and first-deviation detection: implemented for the practice agent
- Safety enforcement: implemented; tests prove blocked/review actions never reach a tool
- Incident retrieval and prediction: implemented; model trained on synthetic fault-injection traces,
  evaluated on held-out bug families (see `results/evaluation/`)
- LLM investigation: implemented for Gemini; scripted fallback when no key is configured
- Bounded patching, tests and replay: implemented in disposable sandbox copies
- Streamlit dashboard: implemented

Limitations: one small practice agent; the training data is synthetic (labels come from injected
faults), so model scores show generalisation across bug families of this agent only.

See `BIFURA_MASTER_PROJECT_SPEC.md` and `BIFURA_EXECUTION_PLAN.md` for the authoritative requirements and implementation order.