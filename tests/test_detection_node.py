import sys
from pathlib import Path
import json

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.nodes.rag_node import rag_node
from src.nodes.detection_node import detection_node


unsafe_state = {
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


safe_state = {
    "cleaned_code": """
import sqlite3

def login(username, password):
    conn = sqlite3.connect("users.db")
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    result = conn.execute(query, (username, password)).fetchone()
    return result
""",
    "application_context": "This is a login function for a web application that handles user authentication."
}


print("\n===== UNSAFE SAMPLE: RAG STEP =====")
unsafe_with_rag = rag_node(unsafe_state)
print(unsafe_with_rag["retrieved_context"])

print("\n===== UNSAFE SAMPLE: DETECTION STEP =====")
unsafe_result = detection_node(unsafe_with_rag)
print(json.dumps(unsafe_result["detection_result"], indent=2))


print("\n===== SAFE SAMPLE: RAG STEP =====")
safe_with_rag = rag_node(safe_state)
print(safe_with_rag["retrieved_context"])

print("\n===== SAFE SAMPLE: DETECTION STEP =====")
safe_result = detection_node(safe_with_rag)
print(json.dumps(safe_result["detection_result"], indent=2))