import os
from collections import Counter

import pandas as pd
import streamlit as st

from src.content.boundary_layer import COURSE, QUESTIONS
from src.content.lab import LAB_NAME, LAB_TASKS
from src.data.synthetic_students import STUDENTS
from src.graph import build_learning_graph
from src.lab_groups import propose_groups

BRAND_NAME = "Lumora"
BRAND_TAGLINE = "Illuminate understanding. Turn knowledge into practice."

st.set_page_config(
    page_title=f"{BRAND_NAME} | AI Learning Prototype",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Safe secret handoff. Nothing is written back to disk.
for key in ("OPENAI_API_KEY", "OPENAI_MODEL", "LANGSMITH_TRACING", "LANGSMITH_API_KEY", "LANGSMITH_PROJECT"):
    try:
        if key in st.secrets and str(st.secrets[key]).strip():
            os.environ[key] = str(st.secrets[key])
    except Exception:
        pass

st.markdown(
    """
<style>
.block-container {max-width: 1180px; padding-top: 1.45rem; padding-bottom: 3rem;}
.lumora-kicker {font-size:.76rem; letter-spacing:.14em; text-transform:uppercase; color:#6c4ce5; font-weight:800;}
.lumora-hero {padding:1.45rem 1.55rem; border:1px solid #e8e2fb; border-radius:22px; background:linear-gradient(120deg,#fbf9ff 0%,#f0f7ff 48%,#f4fff9 100%); margin-bottom:1rem; position:relative; overflow:hidden;}
.lumora-hero:after {content:"✦"; position:absolute; right:1.2rem; top:.1rem; font-size:5.4rem; color:rgba(108,76,229,.10); transform:rotate(10deg);}
.lumora-hero h1 {margin:.12rem 0 .16rem 0; color:#1f2440; font-size:2.45rem; letter-spacing:-.035em;}
.lumora-sub {color:#56617a; font-size:1.06rem; margin-bottom:0; max-width:760px;}
.lumora-flow {display:flex; flex-wrap:wrap; gap:.45rem; margin:.85rem 0 1.1rem 0;}
.lumora-step {display:inline-block; border:1px solid #e3def7; background:#fff; color:#4e4770; border-radius:999px; padding:.32rem .64rem; font-size:.78rem; font-weight:700;}
.lumora-card {border:1px solid #e6e8f0; border-radius:16px; padding:1rem 1.08rem; background:#ffffff; margin:.35rem 0 .85rem 0; box-shadow:0 1px 2px rgba(25,28,50,.025);}
.lumora-card strong {color:#232842;}
.lumora-tag {display:inline-block; background:#f0edff; color:#5b42c7; border-radius:999px; padding:.24rem .58rem; font-size:.78rem; font-weight:700; margin-right:.3rem;}
.lumora-muted {color:#70798d; font-size:.9rem;}
.lumora-gap {border-left:4px solid #f0a44b; padding-left:.9rem;}
.lumora-ok {border-left:4px solid #41a477; padding-left:.9rem;}
div[data-testid="stMetric"] {border:1px solid #e7e8f1; border-radius:14px; padding:.68rem .82rem; background:white;}
section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] h3 {color:#302a59;}
</style>
""",
    unsafe_allow_html=True,
)

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None
if "review_status" not in st.session_state:
    st.session_state.review_status = "Needs review"

api_key_available = bool(os.getenv("OPENAI_API_KEY", "").strip())
api_model_available = bool(os.getenv("OPENAI_MODEL", "").strip())
live_ai_available = api_key_available and api_model_available

with st.sidebar:
    st.markdown("### ✦ Lumora")
    view = st.radio("View", ["Student", "Instructor", "How it works"], label_visibility="collapsed")
    st.divider()
    st.caption("PUBLIC PROTOTYPE")
    st.write("Advanced Fluid Mechanics")
    st.write("Boundary-Layer Theory")
    st.write("Pipe-Flow Laboratory")
    st.divider()
    if live_ai_available:
        st.success("Live AI evaluation configured")
    elif api_key_available:
        st.info("API key detected; add OPENAI_MODEL to enable Live AI")
    else:
        st.info("Deterministic demo works without an API key")
    st.caption("All student records shown in this public demo are synthetic.")

st.markdown(
    """
<div class="lumora-hero">
  <div class="lumora-kicker">Instructor-guided AI learning</div>
  <h1>Lumora</h1>
  <p class="lumora-sub">Illuminate understanding. Turn knowledge into practice.</p>
</div>
<div class="lumora-flow" aria-label="Lumora learning workflow">
  <span class="lumora-step">Learn</span>
  <span class="lumora-step">Insight</span>
  <span class="lumora-step">Bridge</span>
  <span class="lumora-step">Lab</span>
</div>
""",
    unsafe_allow_html=True,
)


def run_student_graph(answers, confidence, ai_mode):
    graph = build_learning_graph()
    initial = {
        "student_id": "DEMO-001",
        "student_name": "Student A",
        "answers": answers,
        "confidence": confidence,
        "prior_lab_roles": ["Data analysis", "Results interpretation", "Data analysis"],
        "limited_opportunities": ["Pump and valve operation", "Pressure measurement"],
        "ai_mode": ai_mode,
        "errors": [],
    }
    return graph.invoke(initial)


if view == "Student":
    top1, top2 = st.columns([1.55, 1])
    with top1:
        st.markdown("## Lumora Learn")
        st.write("Complete a short diagnostic. The goal is not just a score: Lumora looks for evidence of what to practice and what to ask your instructor next.")
    with top2:
        mode_options = ["Deterministic demo"] + (["Live AI"] if live_ai_available else [])
        ai_mode = st.selectbox(
            "Reasoning evaluator",
            mode_options,
            help="Objective items are always scored deterministically. Written reasoning can optionally use a configured OpenAI model.",
        )

    with st.expander("Learning objectives", expanded=False):
        for objective in COURSE["objectives"]:
            st.markdown(f"- {objective}")

    with st.form("diagnostic_form"):
        answers = {}
        confidence = {}
        for idx, q in enumerate(QUESTIONS, start=1):
            st.markdown(f"### {idx}. {q['prompt']}")
            if q["kind"] == "mcq":
                answers[q["id"]] = st.radio(
                    "Select one",
                    q["options"],
                    key=f"answer_{q['id']}",
                    index=None,
                    label_visibility="collapsed",
                )
            else:
                answers[q["id"]] = st.text_area(
                    "Your reasoning",
                    key=f"answer_{q['id']}",
                    height=95,
                    placeholder="Explain the physical reasoning in your own words...",
                    label_visibility="collapsed",
                )
            confidence[q["id"]] = st.slider(
                "How confident are you?",
                1,
                5,
                3,
                key=f"conf_{q['id']}",
                help="1 = very uncertain, 5 = very confident",
            )
            st.divider()
        submitted = st.form_submit_button("Illuminate my learning evidence", type="primary", use_container_width=True)

    if submitted:
        missing = [q["id"] for q in QUESTIONS if q["kind"] == "mcq" and not answers.get(q["id"])]
        if missing:
            st.error("Please answer all multiple-choice questions before submitting.")
        else:
            with st.spinner("Mapping responses to the instructor-defined concept map..."):
                st.session_state.latest_result = run_student_graph(answers, confidence, ai_mode)

    result = st.session_state.latest_result
    if result:
        feedback = result["student_feedback"]
        st.markdown("---")
        st.markdown("## Lumora Insight")
        m1, m2, m3 = st.columns(3)
        m1.metric("Diagnostic evidence", f"{int(result['overall_score'])}%")
        m2.metric("Possible gaps", len(result.get("knowledge_gaps", [])))
        m3.metric("Reasoning mode", result.get("written_evaluation", {}).get("q4", {}).get("mode", "Demo"))

        if result.get("knowledge_gaps"):
            st.markdown(
                f"""<div class="lumora-card lumora-gap"><strong>Possible knowledge gap</strong><br>
                {feedback['summary']}<br><br><span class="lumora-muted"><strong>Evidence focus:</strong> {feedback['focus']}</span></div>""",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='lumora-card lumora-ok'><strong>Current evidence</strong><br>{feedback['summary']}</div>",
                unsafe_allow_html=True,
            )

        c1, c2 = st.columns([1.15, 1])
        with c1:
            st.markdown("### Lumora Bridge — questions for class")
            for i, question in enumerate(feedback["questions"], start=1):
                st.markdown(f"**{i}.** {question}")
            st.caption(feedback["stopping_rule"])
        with c2:
            st.markdown("### Evidence, not labels")
            rows = []
            for qid, item in result.get("written_evaluation", {}).items():
                rows.append(
                    {
                        "Item": qid.upper(),
                        "Rubric evidence": f"{item.get('score', 0)}/3",
                        "Assessment": item.get("gap_type", ""),
                        "Mode": item.get("mode", ""),
                    }
                )
            if rows:
                st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
            if result.get("errors"):
                st.info(" ".join(result["errors"]))

        st.markdown("## Lumora Lab")
        assignment = result["lab_assignment"]
        l1, l2 = st.columns([1, 1.4])
        with l1:
            st.markdown(
                f"""<div class="lumora-card"><span class="lumora-tag">Proposed role</span><br><br>
                <strong>{assignment['task']}</strong><br>{assignment['skill']}<br><br>
                <span class="lumora-muted">Safety level: {assignment['safety']} · Estimated time: {assignment['minutes']} min</span></div>""",
                unsafe_allow_html=True,
            )
        with l2:
            st.markdown("**Why this task?**")
            st.write(assignment["rationale"])
            st.caption(assignment["status"])

elif view == "Instructor":
    st.markdown("## Lumora Insight — Instructor Dashboard")
    st.write("See class-wide patterns, inspect evidence, and keep the instructor in control of interpretation and lab assignments.")

    gap_counts = Counter(s["primary_gap"] for s in STUDENTS if s["primary_gap"] != "No major gap")
    avg_score = round(sum(s["score"] for s in STUDENTS) / len(STUDENTS), 1)
    high_mismatch = sum(s["confidence_mismatch"] == "High" for s in STUDENTS)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Synthetic students", len(STUDENTS))
    c2.metric("Mean diagnostic", f"{avg_score}%")
    c3.metric("High confidence mismatch", high_mismatch)
    c4.metric("Most common gap", gap_counts.most_common(1)[0][0])

    left, right = st.columns([1.05, 1])
    with left:
        st.markdown("### Class-level difficulty patterns")
        gap_df = pd.DataFrame([{"Concept": k, "Students": v} for k, v in gap_counts.items()]).sort_values("Students", ascending=False)
        st.bar_chart(gap_df.set_index("Concept"))
    with right:
        st.markdown("### Students needing targeted review")
        display_df = pd.DataFrame(STUDENTS)[["name", "score", "primary_gap", "confidence_mismatch"]]
        display_df.columns = ["Student", "Score", "Primary signal", "Confidence mismatch"]
        st.dataframe(display_df, hide_index=True, use_container_width=True, height=300)

    st.markdown("### Student evidence review")
    selected_name = st.selectbox("Select synthetic student", [s["name"] for s in STUDENTS])
    student = next(s for s in STUDENTS if s["name"] == selected_name)
    r1, r2, r3 = st.columns(3)
    r1.metric("Diagnostic", f"{student['score']}%")
    r2.metric("Readiness", f"{int(student['readiness'] * 100)}%")
    r3.metric("Confidence mismatch", student["confidence_mismatch"])

    e1, e2 = st.columns([1.2, 1])
    with e1:
        st.markdown(
            f"""<div class="lumora-card lumora-gap"><strong>{student['gap_type']}</strong><br>
            Possible area: {student['primary_gap']}<br><br>
            <span class="lumora-muted">This public dashboard uses synthetic evidence. In a live course, the original response would appear here beside the AI summary.</span></div>""",
            unsafe_allow_html=True,
        )
        review = st.radio(
            "Instructor interpretation",
            ["Agree", "Needs follow-up", "Not a knowledge gap", "Uncertain"],
            horizontal=True,
        )
        st.text_area("Instructor note", placeholder="Add context, correct the AI, or record a follow-up question...")
        if st.button("Save review decision", type="primary"):
            st.session_state.review_status = review
            st.success(f"Review recorded in this session: {review}")
    with e2:
        st.markdown("**Prior practical evidence**")
        st.write("Prior roles: " + ", ".join(student["prior_lab_roles"]))
        st.write("Limited opportunity: " + ", ".join(student["limited_opportunities"]))
        st.caption("Fairness rule: no opportunity ≠ lack of skill.")

    st.markdown(f"## Lumora Lab — {LAB_NAME}")
    task_df = pd.DataFrame(LAB_TASKS)[["task", "skill", "safety", "minutes"]]
    task_df.columns = ["Task", "Skill / evidence", "Safety", "Minutes"]
    st.dataframe(task_df, hide_index=True, use_container_width=True)

    groups = propose_groups(STUDENTS, group_size=3)
    st.markdown("### Proposed complementary groups")
    group_cols = st.columns(2)
    for i, group in enumerate(groups):
        with group_cols[i % 2]:
            st.markdown(f"**{group['group']}**")
            for role in group["members"]:
                st.write(f"• {role['student']} — {role['task']}")

    a1, a2 = st.columns([1, 2])
    with a1:
        approved = st.checkbox("I reviewed safety and task coverage")
        if st.button("Approve proposed lab plan", disabled=not approved, use_container_width=True):
            st.success("Lab plan approved for this demo session.")
    with a2:
        st.info("Lumora proposes roles; the instructor remains the final decision-maker and can override any assignment.")

else:
    st.markdown("## How Lumora works")
    st.write("Lumora uses a small stateful graph rather than a single all-purpose chatbot. Deterministic scoring handles objective evidence; model reasoning is reserved for interpretation of written explanations when enabled.")

    st.code(
        "START → score objective answers → evaluate written reasoning → map concepts → identify possible gaps → student feedback → instructor summary → lab assignment → END",
        language="text",
    )

    cols = st.columns(4)
    with cols[0]:
        st.markdown("### 1 · Learn")
        st.write("Five-question boundary-layer diagnostic with confidence reporting.")
    with cols[1]:
        st.markdown("### 2 · Insight")
        st.write("Concept-level evidence is translated into tentative learning signals.")
    with cols[2]:
        st.markdown("### 3 · Bridge")
        st.write("Focused questions turn uncertainty into productive instructor discussion.")
    with cols[3]:
        st.markdown("### 4 · Lab")
        st.write("Opportunity-aware task assignment plus instructor review and override.")

    st.markdown("### Prototype guardrails")
    st.markdown(
        """
- **Synthetic data only** in the public demonstration.
- **Possible gaps, not definitive labels.** Original evidence should remain visible.
- **Bounded remediation.** Persistent or ambiguous gaps are routed toward instructor discussion.
- **No automated high-stakes grading.** Personalized support stays under a common instructor-defined competency framework.
- **Opportunity before evaluation.** A student is not marked deficient simply because they were never given a practical task.
"""
    )

st.divider()
st.caption("Lumora · Public concept prototype · Human-guided, evidence-based, opportunity-aware learning")
