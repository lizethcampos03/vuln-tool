def preprocess_node(state):
    new_state = dict(state)

    code = state.get("code", "")

    cleaned = code.strip()

    new_state["cleaned_code"] = cleaned
    new_state["code_length"] = len(cleaned)

    return new_state