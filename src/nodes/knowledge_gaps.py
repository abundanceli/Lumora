from typing import Any

from src.content.boundary_layer import CONCEPTS, GAP_TAXONOMY


def map_knowledge_gaps(state: dict[str, Any]) -> dict[str, Any]:
    evidence: dict[str, dict[str, Any]] = {}
    gaps: list[dict[str, Any]] = []
    confidence = state.get("confidence", {})

    for qid, result in state.get("objective_results", {}).items():
        concept = result["concept"]
        correct = bool(result["correct"])
        student_conf = int(confidence.get(qid, 3))
        entry = evidence.setdefault(concept, {"correct": 0, "attempts": 0, "notes": []})
        entry["attempts"] += 1
        entry["correct"] += int(correct)
        entry["notes"].append(f"{qid.upper()}: {'correct' if correct else 'incorrect'}; confidence {student_conf}/5")
        if not correct:
            gap_type = "conceptual_misunderstanding"
            if concept == "no_slip":
                gap_type = "boundary_condition_error"
            gaps.append({
                "concept": concept,
                "concept_label": CONCEPTS[concept]["label"],
                "gap_type": gap_type,
                "gap_label": GAP_TAXONOMY[gap_type],
                "assessment_confidence": "high" if student_conf >= 4 else "moderate",
                "evidence": f"Incorrect objective response with self-reported confidence {student_conf}/5.",
            })

    for qid, result in state.get("written_evaluation", {}).items():
        concept = result["concept"]
        entry = evidence.setdefault(concept, {"correct": 0, "attempts": 0, "notes": []})
        entry["attempts"] += 1
        entry["correct"] += int(result.get("score", 0) >= 2)
        entry["notes"].append(f"{qid.upper()}: {result.get('evidence', '')}")
        gap_type = result.get("gap_type", "uncertain")
        if gap_type != "none":
            gaps.append({
                "concept": concept,
                "concept_label": CONCEPTS[concept]["label"],
                "gap_type": gap_type,
                "gap_label": GAP_TAXONOMY.get(gap_type, GAP_TAXONOMY["uncertain"]),
                "assessment_confidence": result.get("confidence", "moderate"),
                "evidence": result.get("needs", result.get("evidence", "Written reasoning needs review.")),
            })

    # Consolidate duplicate concepts, preferring written-evidence gaps.
    consolidated: dict[str, dict[str, Any]] = {}
    for gap in gaps:
        consolidated[gap["concept"]] = gap

    return {"concept_evidence": evidence, "knowledge_gaps": list(consolidated.values())}
