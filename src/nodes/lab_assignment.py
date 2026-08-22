from typing import Any

from src.content.lab import LAB_TASKS


def _task_by_name(name: str) -> dict[str, Any] | None:
    for task in LAB_TASKS:
        if task["task"] == name:
            return task
    return None


def prepare_lab_assignment(state: dict[str, Any]) -> dict[str, Any]:
    limited = state.get("limited_opportunities", []) or []
    prior = state.get("prior_lab_roles", []) or []

    # Opportunity-first: choose a safe task the learner has had limited opportunity to perform.
    candidate_names = [
        "Pump and valve operation",
        "Pressure measurement",
        "Flow-rate measurement",
        "Equipment inspection",
        "Troubleshooting",
        "Uncertainty analysis",
        "Results interpretation",
        "Reynolds-number calculation",
    ]
    selected = None
    for name in candidate_names:
        if name in limited:
            selected = _task_by_name(name)
            if selected:
                break

    if selected is None:
        # Rotate away from the most repeated prior role.
        selected = _task_by_name("Equipment inspection")
        if prior.count("Data analysis") >= 2:
            selected = _task_by_name("Pump and valve operation")

    gaps = state.get("knowledge_gaps", [])
    rationale_parts = ["Selected to increase hands-on opportunity rather than simply reward the strongest existing skill."]
    if prior:
        rationale_parts.append(f"Prior roles include: {', '.join(prior[-3:])}.")
    if limited:
        rationale_parts.append(f"Limited prior opportunity recorded for: {', '.join(limited)}.")
    if gaps:
        rationale_parts.append("The assignment remains separate from high-stakes grading; concept gaps are used only as readiness context.")

    return {
        "lab_assignment": {
            "task": selected["task"],
            "skill": selected["skill"],
            "safety": selected["safety"],
            "prerequisites": selected["prerequisites"],
            "minutes": selected["minutes"],
            "rationale": " ".join(rationale_parts),
            "status": "Proposed — instructor approval required",
        }
    }
