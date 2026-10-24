# Bifura: how to run it and present it

## 0. One-time setup (Command Prompt, in this folder)

```cmd
py -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[dev]"
```

### Connect Gemini (the investigator's LLM)

1. Get a free API key at https://aistudio.google.com → **Get API key**.
2. Copy `.env.example` to `.env` (same folder as `app.py`).
3. Put your key in it: `GEMINI_API_KEY=your_key_here`
   (optional: `LLM_MODEL=gemini-2.5-flash` to pin a model; empty = newest stable "flash" model).
4. Start (or restart) the app. The sidebar shows **Gemini connected**.

Without a key everything still works in **scripted mode**: same tools, same safety gate,
same verification, but the investigator follows a fixed script with the scenario's known fix.
It is labelled "Scripted investigator" everywhere, so it is never mistaken for Gemini.

## 1. Start the dashboard

```cmd
.venv\Scripts\activate
streamlit run app.py
```

Open http://localhost:8501. Make sure no older copy of Bifura (for example one in Downloads)
is still running on that port; stop it with Ctrl+C first.

## 2. What you see

| Where | What it is |
|-------|-----------|
| **Left sidebar** (Streamlit) | "Bifura Debugger": controls, numbers 1-4 below |
| **Main area, left** | The investigation story: 8 steps that play like a guided walkthrough |
| **Main area, right** | The causal-impact graph of the agent's run |
| **Top right ▯ button** | Opens the Deep dive panel for the selected step |

## 3. Run a live investigation (sidebar section 1)

1. **Scenario**: pick which bug is injected into the practice agent:
   - *ACME (separator bug)*: "12,400" is read as 1,240.
   - *Globex (swapped arguments)*: growth is calculated with current and previous swapped.
   - *Initech (wrong step order)*: the report is written before growth is calculated.
2. **Investigate with Gemini**: on when a key is set.
3. Click **▶ Run agent & investigate**. The sidebar streams each step live:
   - the practice agent runs with Bifura tracing attached (no manual trace export);
   - Bifura finds the first deviation and the trained model predicts the failure type;
   - Gemini investigates: every tool call it proposes is checked by the safety policy
     (✓ ALLOW / ⏸ REVIEW / ✗ BLOCK). A scripted policy check also tries to read `.env`, and it is blocked;
   - Gemini patches the **sandbox copy** only, then Bifura re-runs the tests and replays the run itself.
4. When it finishes, the new run opens and plays in the main area.

## 4. Show a run (sidebar section 2)

- **Run**: any live run (newest first) or the recorded R-0412 sample.
- **Playback: Auto / Step**: Step stops after each step; press **→** to continue.
- **Autoplay**: start playing as soon as the run opens; otherwise click **Run investigation**.

## 5. Learning & prediction (sidebar section 3)

- **Held-out macro-F1**: how well the trained model (TF-IDF + Logistic Regression) predicts
  the failure type on **bug families it never saw in training**, compared with always guessing the
  most common class. **Top-2 accuracy**: how often the right type is in its first two guesses.
- **Evaluation details**: per-class scores, confusion matrix, and the expert-rules reference.
- **Retrain on a new dataset version**: re-runs the agent with all 16 fault families on random
  inputs, adds the live incidents you approved, trains, evaluates, and promotes the model only if it
  beats the baseline.

## 6. Incident memory (sidebar section 4)

Every live investigation is saved as an incident. Verified ones show an **Approve** button;
approving lets that incident into the next training dataset. Nothing trains on unreviewed data.

## 6a. Choosing what to check

The first choice in the sidebar, **What do you want to check?**:

| Choice | Use it for |
|---|---|
| 🧪 **ACME agent (bug demo)** | Bifura debugs a small AI program (sections 3–6 above) |
| ⚡ **KVL circuit check** | Check KVL equations from a chat, an AI, or yourself (6b) |
| 💬 **Numeric chat check** | Check an AI's step-by-step calculation (6c) |

## 6b. KVL circuit check

1. **The circuit**: keep *Example: coupled inductors (your circuit)*, or choose *Upload my own circuit
   picture* and click **Read the circuit with AI**. The table on the right is what Bifura will use:
   check it against the picture, **especially which end each dot is on**, and edit any cell if needed.
2. **Bifura's correct KVL**: hidden, so you can try first. Open it to see each loop's equation and a
   reason for every term (self term, mutual term, sign from the dot convention).
3. Three tabs:
   - **📋 Check a chat I had**: paste a chat (or upload a .txt). **Load my example chat** loads your Gemini
     chat. Bifura finds every equation, says who wrote it, marks it ✅/❌, shows the wrong terms
     (written vs correct) and the first message with a mistake. "Why?" explains each wrong term.
   - **🤖 Ask an AI to write KVL**: the AI gets the picture + circuit data and writes the equations
     (no solving). Bifura checks them, tells the AI *which* terms are wrong (not the answer), and lets
     it try again up to 2 times. Only a fully correct answer for every loop is marked ✓ Verified.
   - **✍️ Check my own equation**: type an equation and get an instant check (no AI needed).

You can write equations naturally: `L1*di1/dt`, `L1 di1/dt`, `M*d(i1-i2)/dt`, `Md(i1 - i2)/dt`,
`v1(t)`, LaTeX `\frac{di_1}{dt}`, and even copy-pasted text like `L1dtdi1`. Multiplying the whole
equation by −1 or moving terms across `=` is fine.

What Bifura found in your Gemini chat: all 4 of Gemini's KVL equations were wrong (the mutual-inductance
signs), and your own equation (message 7) is correct.

## 6c. Numeric chat check: let Bifura check Gemini, GPT or Claude

At the top of the sidebar, choose **💬 Numeric chat check**.

1. **AI model**: Gemini works with your key. For GPT or Claude, add `OPENAI_API_KEY` or
   `ANTHROPIC_API_KEY` to `.env`, run `pip install openai` / `pip install anthropic`, and restart.
2. **Demo: make the AI slip one mistake**: asks the AI to put one realistic calculation slip in its
   answer, so a demo always has something to catch. It is labelled "demo" in the results.
3. **Expected final answer** (optional): like a teacher's answer key, e.g. `16 W`.
4. Type a numerical problem in the chat box, or click an example
   (series circuit, voltage divider, two-loop KVL).

What happens:
- The AI answers step by step (each step is `name = formula = value`).
- Bifura recalculates **every step exactly** (SymPy calculator) and shows a table: ✅ correct,
  ❌ first wrong step, ⚠️ wrong only because it used an earlier wrong number.
- It guesses the type of slip (sign error, power-of-10 slip, swapped operator, upside-down division…).
- It tells the AI exactly which step is wrong and asks it to redo the solution (up to 2 times),
  then checks the new answer again. Only then does it say **✓ Verified**.
- **▶ Watch it in the story view** plays the same check in the animated story + graph.

Limit: Bifura proves *calculation* mistakes. If the AI uses the wrong formula but calculates it
correctly, only the expected answer catches it, so give one when you know it.

Demo tip: the **Two-loop circuit with KVL** example with expected answer `1.538` is a good one.
In our tests Gemini got it wrong even without demo mode, and Bifura caught it and got it corrected.

## 7. Controls inside the story

| Control | Key | What it does |
|---------|-----|--------------|
| Run investigation / ▶ | Space | Start, or pause / resume |
| › (Step mode) | → | Next step |
| ↻ | R | Restart |
| 1× / 1.5× / 2× | | Speed |
| Auto / Step | S | Play straight through or stop after each step |
| Plain English / Engineer | | Plain explanation or technical detail |
| Click a step's link or a graph box | | Opens the Deep dive (Overview, Data flow, Evidence, Raw event) |
| Esc / ← → | | Close the Deep dive / move between steps |
| **⟨ Hide controls** (top of sidebar) / **☰ Controls** (top left) | | Hide or show the left sidebar; the story keeps playing |
| **Hide story / Show story** (left of the run title) | G | Hide or show the middle story panel |
| **Expand graph / Exit full graph** (top right of the graph) | G | Give the graph the full width, or shrink it back |
| Double-click the graph | | Zoom the graph back to fit |

## 8. Suggested 3-minute demo

1. "A revenue agent reported ACME's growth as −88%. The right answer is about +18%."
2. Pick *ACME*, click **Run agent & investigate** and point at the live log: tracing, deviation,
   prediction, Gemini's tool calls, the blocked `.env` read, the patch, the verification.
3. Switch Playback to **Step** and walk through the 8 steps: first deviation at extract_revenue,
   prediction *state_or_dataflow*, 3 agent steps inherited the bad value, Gemini's fix on agent.py:38,
   tests 5/5 and replay +18.1%.
4. Open **Learning & prediction**: the model is tested on unseen bug families; show the numbers honestly.
5. Approve the new incident, click **Retrain**, and show the dataset version goes up.

## 9. Command line

```cmd
python -m bifura.pipeline revenue_separator             :: live investigation (Gemini if key set)
python -m bifura.pipeline growth_args --scripted        :: without the LLM
python -m bifura.learning.lifecycle                     :: build dataset + train + evaluate
python -m bifura.dashboard results\dashboard.html       :: standalone HTML export
python -m pytest -q                                     :: all tests
```
