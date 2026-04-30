"""
Test: Input Node

Purpose:
Verifies that the input node correctly initializes the pipeline state
with raw code and optional context.

Expected Behavior:
- Input code is preserved
- Context is correctly attached to state
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from nodes.input_node import input_node


def test_input_node_basic():
    test_state = {
        "code": "print('test')",
        "context": "simple"
    }

    result = input_node(test_state)

    assert result["code"] == "print('test')"
    assert result["context"] == "simple"


def test_input_node_missing_fields():
    test_state = {}

    result = input_node(test_state)

    assert result["code"] == ""
    assert result["context"] == ""