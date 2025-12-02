# backend/src/agent/nodes/filter.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from typing import List
from ..state import AgentState
from ..models import Product
import os
import json

# 1. Setup the "Fast" Model
# Use 'gemini-2.5-flash' for speed/cost, or your specific 2.5 version
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0,
    google_api_key=os.environ["GOOGLE_API_KEY"]
)

# 2. Define the Output Schema (A list of products)
class CuratedList(BaseModel):
    items: List[Product] = Field(description="The top valid products found")

# 3. The Prompt
FILTER_PROMPT = """You are a Strict Quality Control Shopper.
You will receive a list of raw web search results.

Your Goal: Filter this list down to the best 3-5 actual products for sale.

Rules:
1. REMOVE Blog posts, Reviews, YouTube videos, and Articles. We only want 'Add to Cart' style pages.
2. REMOVE items with NO image. (We need visuals).
3. REMOVE items strictly outside the user's budget (if specified).
4. DEDUPLICATE: If the same product appears twice (e.g. from Amazon and BestBuy), keep the cheaper one.
5. FORMATTING: Ensure 'price' is a clean string like '$299.00'.

User Constraints: {constraints}
"""

def filter_node(state: AgentState):
    print("--- FILTER NODE: Cleaning results ---")
    
    raw_results = state.get("raw_search_results", [])
    plan = state.get("search_plan")
    
    if not raw_results:
        print("  x No items to filter.")
        return {"curated_products": []}

    # Prepare the context for the LLM
    # We serialize the raw data to JSON so the LLM can read it
    raw_text = json.dumps(raw_results, indent=2)
    constraints = f"Max Price: {plan.max_price}, Must Have: {plan.must_have_features}"

    # Invoke LLM
    structured_llm = llm.with_structured_output(CuratedList)
    
    try:
        response = structured_llm.invoke([
            SystemMessage(content=FILTER_PROMPT.format(constraints=constraints)),
            HumanMessage(content=f"Here is the raw search data:\n{raw_text}")
        ])
        
        valid_items = response.items
        print(f"--- Kept {len(valid_items)} valid products (Discarded {len(raw_results) - len(valid_items)}) ---")
        return {"curated_products": valid_items}

    except Exception as e:
        print(f"  x Filter crashed: {e}")
        return {"curated_products": []}