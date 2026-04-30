"""
Input Node — Data Ingestion

Purpose:
This node initializes the pipeline by receiving raw input data,
including the source code to analyze and any optional context.

Inputs:
- code: Raw source code
- context: Optional description of the application

Outputs:
- state containing initial inputs for downstream processing

Role in Pipeline:
Acts as the entry point of the system, ensuring all required inputs
are structured and passed forward consistently.
"""
def input_node(state):
    new_state = dict(state)

    new_state["code"] = state.get("code", "")
    new_state["context"] = state.get("context", "")
    new_state["file_name"] = state.get("file_name", "unknown.py")

    return new_state