# backend/src/app.py
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.graph import graph
import uvicorn

app = FastAPI(title="ShopGraph API")

# Define the Request Body
class SearchRequest(BaseModel):
    query: str

@app.post("/search")
async def search_endpoint(request: SearchRequest):
    print(f"Incoming request: {request.query}")
    
    # Initialize state
    initial_state = {
        "original_query": request.query,
        "messages": [],
        "feedback": {}
    }
    
    # Run the Graph
    try:
        # .invoke() runs the entire workflow (Planner -> Search -> Filter)
        result = graph.invoke(initial_state)
        
        return {
            "status": "success",
            "products": result.get("curated_products", [])
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)