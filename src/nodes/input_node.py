def input_node(state):
    new_state = dict(state)

    new_state["code"] = state.get("code", "")
    new_state["context"] = state.get("context", "")
    new_state["file_name"] = state.get("file_name", "unknown.py")

    return new_state