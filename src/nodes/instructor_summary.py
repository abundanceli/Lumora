from typing import Any


def generate_instructor_summary(state: dict[str, Any]) -> dict[str, Any]:
    gaps = state.get("knowledge_gaps", [])
    if gaps:
        primary = gaps[0]
        headline = f"Possible gap: {primary['concept_label']}"
        evidence = primary["evidence"]
        confidence = primary["assessment_confidence"]
    else:
        headline = "No major gap flagged by this diagnostic"
        evidence = "Objective and written responses did not produce a strong concept-level concern."
        confidence = "moderate"

    return {
        "instructor_summary": {
            "headline": headline,
            "evidence": evidence,
            "confidence": confidence,
            "recommended_action": "Review the original response before confirming the label. Use the summary to target discussion, not to automate grading.",
        }
    }
