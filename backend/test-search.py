# backend/test_search.py
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
load_dotenv()

from agent.nodes.search import search_node
from agent.models import SearchPlan

def test_search():
    print("--- 🧪 TESTING SEARCH NODE ---")
    
    # 1. Mock the State (Pretend the Planner already finished)
    fake_state = {
        "search_plan": SearchPlan(
            search_queries=[
                "Sony WH-1000XM5 price",
                "Bose QuietComfort 45 sale"
            ],
            max_price=300
        ),
        "raw_search_results": []
    }

    # 2. Run the Node
    try:
        result = search_node(fake_state)
        items = result.get("raw_search_results", [])
        
        if items:
            print(f"\n✅ SUCCESS: Found {len(items)} items.")
            print("\n--- First Item Sample ---")
            first_item = items[0]
            print(f"Title: {first_item.get('title')}")
            print(f"URL:   {first_item.get('url')}")
            print(f"Image: {first_item.get('image_url', 'No Image')}")
        else:
            print("❌ Warning: Search ran but returned 0 results.")

    except Exception as e:
        print(f"❌ CRASHED: {e}")

if __name__ == "__main__":
    test_search()