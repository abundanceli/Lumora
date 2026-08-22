import json
import os
import re
from typing import Any

from openai import OpenAI

from src.content.boundary_layer import QUESTIONS


def _question_map() -> dict[str, dict[str, Any]]:
    return {q["id"]: q for q in QUESTIONS}


def score_objective(state: dict[str, Any]) -> dict[str, Any]:
    qmap = _question_map()
    results: dict[str, dict[str, Any]] = {}
    for qid in ("q1", "q2", "q3"):
        q = qmap[qid]
        answer = state.get("answers", {}).get(qid, "")
        correct = answer == q["answer"]
        results[qid] = {
            "correct": correct,
            "concept": q["concept"],
            "answer": answer,
            "expected": q["answer"],
            "evidence": q["explanation"],
        }
    return {"objective_results": results}


def _heuristic_written_eval(qid: str, text: str) -> dict[str, Any]:
    clean = re.sub(r"\s+", " ", (text or "").lower()).strip()
    if not clean:
        return {
            "score": 0,
            "gap_type": "uncertain",
            "confidence": "high",
            "evidence": "No written reasoning was provided.",
            "strength": "No written evidence available yet.",
            "needs": "Provide a brief physical explanation before the system infers mastery.",
        }

    if qid == "q4":
        hits = [
            any(k in clean for k in ["delta", "δ", "thin", "smaller length", "shorter"]),
            any(k in clean for k in ["du/dy", "∂u/∂y", "wall-normal", "normal gradient", "y gradient"]),
            any(k in clean for k in ["larger", "dominant", "1/delta", "1/δ", "scale"]),
        ]
        score = sum(hits)
        if score == 3:
            gap = "none"
            need = "The scaling argument is physically and mathematically connected."
        elif score == 2:
            gap = "physical_interpretation_gap"
            need = "Make the order-of-magnitude comparison explicit: the same velocity change occurs over δ rather than L."
        else:
            gap = "missing_prerequisite"
            need = "Review order-of-magnitude scaling before applying the boundary-layer approximation."
        return {
            "score": score,
            "gap_type": gap,
            "confidence": "moderate" if score == 2 else "high",
            "evidence": f"Detected {score}/3 expected elements in the explanation.",
            "strength": "Recognizes at least part of the thin-layer argument." if score else "The response does not yet show the scaling argument.",
            "needs": need,
        }

    hits = [
        any(k in clean for k in ["pressure increase", "increasing pressure", "dp/dx", "adverse"]),
        any(k in clean for k in ["low momentum", "near wall", "near-wall", "slower fluid"]),
        any(k in clean for k in ["deceler", "reverse", "backflow", "separation", "detach"]),
    ]
    score = sum(hits)
    if score == 3:
        gap = "none"
        need = "The pressure-gradient mechanism is stated clearly."
    elif score == 2:
        gap = "physical_interpretation_gap"
        need = "Connect the adverse pressure gradient specifically to low-momentum near-wall fluid and possible reversal."
    else:
        gap = "conceptual_misunderstanding"
        need = "Revisit how streamwise pressure rise acts against the near-wall momentum balance."
    return {
        "score": score,
        "gap_type": gap,
        "confidence": "moderate" if score == 2 else "high",
        "evidence": f"Detected {score}/3 expected elements in the explanation.",
        "strength": "Recognizes part of the adverse-pressure-gradient mechanism." if score else "The mechanism is not yet supported by the written response.",
        "needs": need,
    }


def _live_written_eval(qid: str, text: str) -> dict[str, Any] | None:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None

    model = os.getenv("OPENAI_MODEL", "").strip()
    if not model:
        return None
    q = _question_map()[qid]
    schema_hint = {
        "score": "integer 0-3",
        "gap_type": "none | missing_prerequisite | conceptual_misunderstanding | mathematical_error | physical_interpretation_gap | assumption_recognition_gap | boundary_condition_error | uncertain",
        "confidence": "low | moderate | high",
        "evidence": "brief evidence-linked sentence",
        "strength": "brief sentence",
        "needs": "brief sentence",
    }
    prompt = f"""You are evaluating a synthetic public-demo response for an Advanced Fluid Mechanics course.
Use only the instructor-defined question and rubric. Do not infer personal traits. Use tentative language.

Question: {q['prompt']}
Rubric: {q.get('rubric', [])}
Student response: {text}

Return JSON only, with this shape:
{json.dumps(schema_hint)}
Score 0-3 according to how many rubric elements are substantively demonstrated.
"""
    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(model=model, input=prompt)
        raw = response.output_text.strip()
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.I | re.S)
        data = json.loads(raw)
        data["score"] = max(0, min(3, int(data.get("score", 0))))
        return data
    except Exception:
        return None


def evaluate_written_reasoning(state: dict[str, Any]) -> dict[str, Any]:
    answers = state.get("answers", {})
    live_requested = state.get("ai_mode") == "Live AI"
    evaluations: dict[str, dict[str, Any]] = {}
    errors: list[str] = list(state.get("errors", []))

    for qid in ("q4", "q5"):
        text = str(answers.get(qid, ""))
        result = _live_written_eval(qid, text) if live_requested else None
        if result is None:
            if live_requested:
                errors.append(f"Live AI evaluation for {qid} was unavailable; deterministic fallback used.")
            result = _heuristic_written_eval(qid, text)
            result["mode"] = "Deterministic demo"
        else:
            result["mode"] = "Live AI"
        result["response"] = text
        result["concept"] = _question_map()[qid]["concept"]
        evaluations[qid] = result

    objective_correct = sum(1 for r in state.get("objective_results", {}).values() if r.get("correct"))
    written_points = sum(r.get("score", 0) for r in evaluations.values())
    overall = round(100 * (objective_correct + written_points / 3) / 5, 0)
    return {"written_evaluation": evaluations, "overall_score": overall, "errors": errors}
