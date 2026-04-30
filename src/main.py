"""
Main Entry Point

Purpose:
Runs the full LangGraph security auditing pipeline from input
to final report.

Usage:
python src/main.py
"""
from langsmith import traceable
from src.nodes.input_node import input_node
from src.nodes.preprocess_node import preprocess_node
from src.nodes.rag_node import rag_node
from src.nodes.detection_node import detection_node
from src.nodes.validation_node import validation_node
from src.nodes.fix_node import fix_node
from src.nodes.output_node import output_node

@traceable(name="vuln_tool_pipeline")
def run_pipeline():
    state = {
    "file_name": "fintech_login.py",
    "code": """
import sqlite3

def login(username, password):
    conn = sqlite3.connect("users.db")
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    result = conn.execute(query).fetchone()
    return result
""",
    "context": "This is a login function for a FinTech web application that handles user authentication and sensitive account access."
}

    state = input_node(state)
    state = preprocess_node(state)
    state = rag_node(state)
    state = detection_node(state)
    state = validation_node(state)
    state = fix_node(state)
    state = output_node(state)

    return state


if __name__ == "__main__":
    result = run_pipeline()
    print(result)