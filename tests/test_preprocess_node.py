import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from nodes.preprocess_node import preprocess_node


def test_preprocess_node_strips_spaces():
    test_state = {
        "code": "   print('test')   "
    }

    result = preprocess_node(test_state)

    assert result["cleaned_code"] == "print('test')"


def test_preprocess_node_missing_code():
    test_state = {}

    result = preprocess_node(test_state)

    assert result["cleaned_code"] == ""