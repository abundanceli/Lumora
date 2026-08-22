from functools import lru_cache

from langgraph.graph import END, START, StateGraph

from src.nodes.evaluation import evaluate_written_reasoning, score_objective
from src.nodes.instructor_summary import generate_instructor_summary
from src.nodes.knowledge_gaps import map_knowledge_gaps
from src.nodes.lab_assignment import prepare_lab_assignment
from src.nodes.student_feedback import generate_student_feedback
from src.state import LearningState


@lru_cache(maxsize=1)
def build_learning_graph():
    graph = StateGraph(LearningState)
    graph.add_node("score_objective", score_objective)
    graph.add_node("evaluate_written_reasoning", evaluate_written_reasoning)
    graph.add_node("map_knowledge_gaps", map_knowledge_gaps)
    graph.add_node("generate_student_feedback", generate_student_feedback)
    graph.add_node("generate_instructor_summary", generate_instructor_summary)
    graph.add_node("prepare_lab_assignment", prepare_lab_assignment)

    graph.add_edge(START, "score_objective")
    graph.add_edge("score_objective", "evaluate_written_reasoning")
    graph.add_edge("evaluate_written_reasoning", "map_knowledge_gaps")
    graph.add_edge("map_knowledge_gaps", "generate_student_feedback")
    graph.add_edge("generate_student_feedback", "generate_instructor_summary")
    graph.add_edge("generate_instructor_summary", "prepare_lab_assignment")
    graph.add_edge("prepare_lab_assignment", END)
    return graph.compile()
