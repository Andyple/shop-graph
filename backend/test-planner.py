import sys
import os
from dotenv import load_dotenv

# 1. Setup the path so we can import from 'src'
# This tells Python: "Look for modules in the 'src' folder right next to me"
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# 2. Load environment variables (API Keys)
load_dotenv()

from agent.nodes.planner import planner_node

def test_planner():
    # 3. Create a Fake State (Mocking what the app would send)
    print("--- 🧪 TESTING PLANNER NODE ---")
    fake_state = {
        "original_query": "best noise cancelling headphones for travel under $300",
        # We leave other fields empty since the planner doesn't need them
        "messages": [],
        "feedback": {} 
    }

    # 4. Run the Node
    try:
        result = planner_node(fake_state)
        
        # 5. Print the Output
        plan = result.get("search_plan")
        if plan:
            print("\n✅ PLAN GENERATED SUCCESSFULLY:")
            print(f"Queries: {plan.search_queries}")
            print(f"Max Price: {plan.max_price}")
            print(f"Must Have: {plan.must_have_features}")
            
            # Print full raw JSON for inspection
            print("\n(Raw JSON):")
            print(plan.model_dump_json(indent=2))
        else:
            print("❌ Error: No plan returned.")
            
    except Exception as e:
        print(f"❌ CRASHED: {e}")

if __name__ == "__main__":
    test_planner()