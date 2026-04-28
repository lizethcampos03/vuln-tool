from nodes.input_node import input_node
from nodes.preprocess_node import preprocess_node
from nodes.rag_node import rag_node
from nodes.detection_node import detection_node
from nodes.validation_node import validation_node
from nodes.fix_node import fix_node
from nodes.output_node import output_node

# Test input
test_state = {
    "code": "   print('hello world')   ",
    "context": "simple test"
}

# Run nodes
state = input_node(test_state)
state.update(preprocess_node(state))
state.update(rag_node(state))
state.update(detection_node(state))
state.update(validation_node(state))
state.update(fix_node(state))
state.update(output_node(state))

print(state["final_report"])