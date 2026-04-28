import sys
from pathlib import Path
import json

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.nodes.rag_node import rag_node
from src.nodes.validation_node import validation_node


test_state = {
    "cleaned_code": """
import sqlite3

def login(username, password):
    conn = sqlite3.connect("users.db")
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    result = conn.execute(query).fetchone()
    return result
""",
    "application_context": "This is a login function for a web application that handles user authentication.",
    "number_of_runs": 10,
    "validation_threshold": 0.5
}

state_with_rag = rag_node(test_state)
validated_state = validation_node(state_with_rag)

print("\n===== VALIDATION RESULT =====")
print(json.dumps(validated_state["validation_result"], indent=2))