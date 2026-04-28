from src.graph import build_graph

def main():
    graph = build_graph()

    sample_state = {
        "data": {
            "file_name": "test_sample.py",
            "code": "user_input = input('Enter: ')\neval(user_input)",
            "context": ""
        }
    }

    result = graph.invoke(sample_state)

    print(result["data"].get("final_report", result["data"]))

if __name__ == "__main__":
    main()