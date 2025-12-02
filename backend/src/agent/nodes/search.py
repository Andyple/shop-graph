# backend/src/agent/nodes/search.py
from tavily import TavilyClient
import os
from ..state import AgentState

# Initialize the client globally (reads from env TAVILY_API_KEY)
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def search_node(state: AgentState):
    print("--- SEARCH NODE: Executing Search Plan ---")
    
    plan = state.get("search_plan")
    if not plan:
        print("Error: No search plan found.")
        return {"raw_search_results": []}

    results = []
    
    # We limit to the top 3 queries to save API credits and time
    queries_to_run = plan.search_queries[:3]
    
    for query in queries_to_run:
        print(f"  > Searching: {query}")
        try:
            # "search_depth='advanced'" digs deeper but is slower. 
            # Use 'basic' for speed if needed.
            response = tavily.search(
                query=query,
                search_depth="advanced",
                max_results=5,
                include_images=True,  # Crucial for your card UI
                include_raw_content=False 
            )
            
            # Tag the results with the query that found them (useful for debugging)
            for item in response.get('results', []):
                item['source_query'] = query
                results.append(item)
                
        except Exception as e:
            print(f"    x Failed to search '{query}': {e}")

    print(f"--- Fetched {len(results)} raw items ---")
    
    # We return the raw list. The Curator Node (next step) will clean it.
    return {"raw_search_results": results}