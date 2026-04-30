"""
RAG Node — Security Knowledge Retrieval

Purpose:
This node retrieves relevant security knowledge from CWE/CVE-based
sources to provide context for vulnerability detection.

Inputs:
- cleaned_code
- application_context (optional)

Outputs:
- retrieved_context: Formatted security knowledge
- retrieved_sources: Structured source metadata

Role in Pipeline:
Enhances detection by grounding the LLM in real-world security
knowledge, improving accuracy and reducing hallucinations.
"""
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