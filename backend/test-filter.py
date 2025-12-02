import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
load_dotenv()

from agent.nodes.filter import filter_node
from agent.models import SearchPlan

def test_filter():
    print("--- 🧪 TESTING FILTER NODE ---")
    
    # 1. Mock Data (Mixed Garbage and Gold)
    fake_state = {
        "search_plan": SearchPlan(
            search_queries=["mock query"], 
            max_price=350.0
        ),
        "raw_search_results": [
            {
                # BAD: A Review Article
                "title": "Sony WH 1000XM5 Review: WORTH IT?",
                "url": "https://recordingnow.com/blog/review",
                "content": "In this article we discuss..."
            },
            {
                # GOOD: A Product
                "title": "Sony WH-1000XM5 Wireless Noise Canceling Headphones, Black",
                "url": "https://amazon.com/sony-xm5",
                "price": "$348.00",
                "image_url": "https://m.media-amazon.com/images/I/51SKmu2G9FL._AC_SL1000_.jpg",
                "content": "Buy Sony headphones. Add to cart."
            },
            {
                # BAD: Too Expensive
                "title": "Gold Plated Sony Headphones",
                "url": "https://luxury.com/gold",
                "price": "$9000.00", 
                "image_url": "http://img.com/gold.png"
            }
        ]
    }

    # 2. Run the Node
    result = filter_node(fake_state)
    products = result.get("curated_products", [])

    # 3. Verify
    print(f"\n✅ Result: {len(products)} products kept.")
    for p in products:
        print(f"  - [${p.price}] {p.title}")
    
    # Simple logic check
    if len(products) == 1 and "Wireless" in products[0].title:
        print("\nPASSED: Successfully filtered out the Blog and the Expensive item.")
    else:
        print("\nFAILED: Logic check failed.")

if __name__ == "__main__":
    test_filter()