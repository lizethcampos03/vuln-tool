"""
LangGraph Workflow Definition

Purpose:
Defines the node sequence and edges for the security auditing pipeline.

Pipeline:
Input → Preprocess → RAG → Detection → Validation → Fix → Output
"""
from langgraph.graph import StateGraph
from typing import TypedDict, Dict, Any

from src.nodes.input_node import input_node
from src.nodes.preprocess_node import preprocess_node
from src.nodes.rag_node import rag_node
from src.nodes.detection_node import detection_node
from src.nodes.validation_node import validation_node
from src.nodes.fix_node import fix_node
from src.nodes.output_node import output_node


class GraphState(TypedDict):
    data: Dict[str, Any]


def build_graph():
    builder = StateGraph(GraphState)

    def wrap(node_fn):
        def wrapped(state):
            current_data = state.get("data", {})
            updated = node_fn(current_data)
            merged = {**current_data, **updated}
            return {"data": merged}
        return wrapped

    builder.add_node("input", wrap(input_node))
    builder.add_node("preprocess", wrap(preprocess_node))
    builder.add_node("rag", wrap(rag_node))
    builder.add_node("detect", wrap(detection_node))
    builder.add_node("validate", wrap(validation_node))
    builder.add_node("fix", wrap(fix_node))
    builder.add_node("output", wrap(output_node))

    builder.set_entry_point("input")

    builder.add_edge("input", "preprocess")
    builder.add_edge("preprocess", "rag")
    builder.add_edge("rag", "detect")
    builder.add_edge("detect", "validate")
    builder.add_edge("validate", "fix")
    builder.add_edge("fix", "output")

    return builder.compile()