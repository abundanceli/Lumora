# Lumora

**Illuminate understanding. Turn knowledge into practice.**

Lumora is an instructor-guided AI learning prototype that connects concept-level learning evidence, focused student–instructor discussion, and equitable hands-on laboratory opportunity.

This repository is intentionally a **narrow public demo**, not a production learning-management system. It demonstrates one complete workflow in **Advanced Fluid Mechanics**:

1. A student completes a five-question boundary-layer diagnostic with confidence reporting.
2. Objective items are scored deterministically.
3. Written reasoning is evaluated against an instructor-defined rubric in deterministic demo mode or optional live-AI mode.
4. Evidence is mapped to possible concept-level knowledge gaps.
5. **Lumora Insight** summarizes the learning evidence without turning it into a definitive label.
6. **Lumora Bridge** produces focused questions for student–instructor discussion.
7. The instructor dashboard shows class-level patterns and explicit review controls.
8. **Lumora Lab** decomposes a pipe-flow laboratory into eight observable tasks and proposes an opportunity-aware individual role while keeping instructor approval in the loop.

## Why Lumora is not a generic chatbot

Lumora uses a small LangGraph workflow with explicit state and node responsibilities:

```text
START
  → score objective answers
  → evaluate written reasoning
  → map responses to concepts
  → identify possible knowledge gaps
  → generate student feedback
  → generate instructor summary
  → prepare lab assignment
END
```

The design deliberately uses deterministic rules where possible and model reasoning only where interpretation is useful.

## Product modules

- **Lumora Learn** — personalized lessons, diagnostics, confidence reporting, and feedback
- **Lumora Insight** — concept-level knowledge-gap evidence and class analytics
- **Lumora Bridge** — focused student–instructor questions and escalation
- **Lumora Lab** — practical task allocation, role rotation, and group formation
- **Lumora Assess** — future adaptive assessment under a shared competency blueprint
- **Lumora Profile** — future permission-controlled longitudinal learning record

## Run locally

Python 3.12 or newer is recommended.

### Windows PowerShell

The commands below do not require changing PowerShell's execution policy:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The application works immediately in **Deterministic demo** mode without any API key.

## Optional: enable live AI evaluation

Create `.streamlit/secrets.toml` locally or add the same values in Streamlit Community Cloud. Do **not** commit a real secrets file.

```toml
OPENAI_API_KEY = "your-key"
OPENAI_MODEL = "your-supported-model-name"
```

Both values are required before the **Live AI** option appears. If a live evaluation fails, Lumora falls back to the deterministic rubric evaluator so the demo remains usable.

## Optional: LangSmith tracing

```toml
LANGSMITH_TRACING = "true"
LANGSMITH_API_KEY = "your-key"
LANGSMITH_PROJECT = "lumora"
```

## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub.
2. Create a new Streamlit Community Cloud app from the repository.
3. Set the entrypoint to `app.py`.
4. Add optional secrets in the app settings.
5. Deploy.

The public prototype is designed to work without secrets, which is the safest default for a portfolio link.

## Public-demo safeguards

- All student records are synthetic.
- AI outputs use tentative language such as **possible knowledge gap**.
- Instructor review is explicit.
- No automated high-stakes grading.
- Practical-skill records distinguish **no opportunity** from **attempted but needs development**.
- Secrets are excluded from version control.

## Repository structure

```text
Lumora/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
└── src/
    ├── graph.py
    ├── state.py
    ├── lab_groups.py
    ├── content/
    │   ├── boundary_layer.py
    │   └── lab.py
    ├── data/
    │   └── synthetic_students.py
    └── nodes/
        ├── evaluation.py
        ├── knowledge_gaps.py
        ├── student_feedback.py
        ├── instructor_summary.py
        └── lab_assignment.py
```

## What comes after the prototype

The next architecture layer is a permission-controlled longitudinal learner profile that transfers structured concept and practical-skill evidence across courses without exposing unrestricted raw interaction history.

---

**Lumora principle:** AI should create better human learning interactions, not replace the instructor or the laboratory.
