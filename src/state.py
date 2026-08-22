from typing import Any, TypedDict


class LearningState(TypedDict, total=False):
    student_id: str
    student_name: str
    answers: dict[str, Any]
    confidence: dict[str, int]
    prior_lab_roles: list[str]
    limited_opportunities: list[str]
    objective_results: dict[str, dict[str, Any]]
    written_evaluation: dict[str, dict[str, Any]]
    concept_evidence: dict[str, dict[str, Any]]
    overall_score: float
    knowledge_gaps: list[dict[str, Any]]
    student_feedback: dict[str, Any]
    instructor_summary: dict[str, Any]
    lab_assignment: dict[str, Any]
    ai_mode: str
    errors: list[str]
