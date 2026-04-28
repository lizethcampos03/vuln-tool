from src.rag.security_knowledge_base import retrieve_security_context, format_retrieved_context


def rag_node(state):
    new_state = dict(state)

    code = state.get("cleaned_code", state.get("code", ""))
    application_context = state.get("application_context", "")

    retrieved_sources = retrieve_security_context(code, application_context)
    retrieved_context = format_retrieved_context(retrieved_sources)

    new_state["retrieved_sources"] = retrieved_sources
    new_state["retrieved_context"] = retrieved_context

    return new_state