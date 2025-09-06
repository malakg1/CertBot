# main.py
import json
from state import State
from graph import build_graph, visualize_graph

if __name__ == "__main__":
    # Optional: visualize the workflow
    visualize_graph()

    # Build and run the app
    app = build_graph()
    initial: State = {
        "trigger": "manual_test",
        "auto_post_linkedin": True,
    }
    result = app.invoke(initial)

    print("\n--- Final State ---")
    print(json.dumps(result, indent=2))
