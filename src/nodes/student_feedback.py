from typing import Any


def generate_student_feedback(state: dict[str, Any]) -> dict[str, Any]:
    gaps = state.get("knowledge_gaps", [])
    score = state.get("overall_score", 0)
    if not gaps:
        summary = "Your responses show solid evidence across the diagnostic concepts. The next step is transfer: explain the assumptions and apply them in a new context."
        focus = "No major concept-level gap identified in this short diagnostic."
    else:
        primary = gaps[0]
        summary = (
            f"Your diagnostic suggests a possible {primary['gap_label'].lower()} in "
            f"{primary['concept_label']}. This is a learning signal, not a final judgment."
        )
        focus = primary["evidence"]

    questions = [
        "Why does the thinness of a boundary layer make the wall-normal viscous term dominant?",
        "How does an adverse pressure gradient reduce the momentum of fluid near the wall?",
        "What additional flow evidence should I examine before concluding that separation has occurred?",
    ]
    return {
        "student_feedback": {
            "score": score,
            "summary": summary,
            "focus": focus,
            "questions": questions,
            "stopping_rule": "If this remains unclear after one focused remediation attempt, bring the question to the instructor rather than looping indefinitely with the AI.",
        }
    }
