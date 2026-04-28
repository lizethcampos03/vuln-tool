import sys
from pathlib import Path
import json

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.nodes.rag_node import rag_node

test_state = {
    "cleaned_code": """
import sqlite3

def login(username, password):
    conn = sqlite3.connect("users.db")
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    result = conn.execute(query).fetchone()
    return result
""",
    "application_context": "This is a login function for a web application that handles user authentication."
}

result = rag_node(test_state)

print("\n===== RETRIEVED CONTEXT =====")
print(result["retrieved_context"])

print("\n===== RETRIEVED SOURCES =====")
print(json.dumps(result["retrieved_sources"], indent=2))