"""
Main Entry Point

Purpose:
Runs the full LangGraph security auditing pipeline from input
to final report.

Usage:
python src/main.py
"""
from dotenv import load_dotenv
load_dotenv()

from langsmith import traceable
import json

from src.nodes.input_node import input_node
from src.nodes.preprocess_node import preprocess_node
from src.nodes.rag_node import rag_node
from src.nodes.detection_node import detection_node
from src.nodes.validation_node import validation_node
from src.nodes.fix_node import fix_node
from src.nodes.output_node import output_node

@traceable(name="vuln_tool_calibration_case")
def run_pipeline(state):
    state = input_node(state)
    state = preprocess_node(state)
    state = rag_node(state)
    state = detection_node(state)
    state = validation_node(state)
    state = fix_node(state)
    state = output_node(state)
    return state


if __name__ == "__main__":
    with open("experiments/calibration_dataset/calibration_cases.json") as f:
        cases = json.load(f)

    for case in cases:
        print(f"\n===== RUNNING {case['id']} =====")

        state = {
            "code": case["code"],
            "context": case["context"],
            "file_name": case["file_name"]
        }

        result = run_pipeline(state)

        print(result)