"""
Preprocess Node — Code Preparation

Purpose:
This node cleans and standardizes the input code to ensure it is
ready for analysis.

Inputs:
- code: Raw source code

Outputs:
- cleaned_code: Trimmed and normalized code

Role in Pipeline:
Ensures consistent formatting and removes noise so downstream
nodes (especially detection) operate reliably.
"""
def preprocess_node(state):
    new_state = dict(state)

    code = state.get("code", "")

    cleaned = code.strip()

    new_state["cleaned_code"] = cleaned
    new_state["code_length"] = len(cleaned)

    return new_state