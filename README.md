# Shop Graph

An app that utilizes AI-Agents to help you shop online.

## Backend

The backend is built with Python using FastAPI, LangChain, and LangGraph.

### Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Andyple/shop-graph.git
    cd shop-graph
    ```
2.  **Set up the environment:**
    - Create a `.env` file in the `backend` directory and add the necessary environment variables (e.g., API keys).
3.  **Install dependencies and run the backend:**
    - Ensure you have `uv` installed. If not, you can install it via `pip install uv` or `curl -sSfL https://astral.sh/uv/install.sh | sh`.
    - Install the project dependencies using `uv` from the `uv.lock` file:
    ```bash
    uv sync
    ```
    - Run the FastAPI application:
    ```bash
    uv run backend/src/app.py
    ```

## API Documentation

Once the application is running, you can interact with the API.

### POST /search

This endpoint takes a user's search query and returns a list of curated products.

**Request Body:**

```json
{
  "query": "your search query here"
}
```

**Example Request (using curl):**

```bash
curl -X POST "http://localhost:8000/search"
    -H "Content-Type: application/json"
    -d '{"query": "high-quality wireless headphones"}'
```

**Success Response:**

```json
{
  "status": "success",
  "products": [
    {
      "name": "Product A",
      "description": "Description of Product A",
      "price": "199.99"
    },
    {
      "name": "Product B",
      "description": "Description of Product B",
      "price": "249.99"
    }
  ]
}
```

## Frontend (Future)

An Android application is planned for the future.

## Folder Structure

```
.
├── backend
│   └── src
│       ├── agent       # Core agent logic using LangGraph
│       ├── api         # FastAPI endpoints
│       └── core        # Core components and utilities
├── mobile              # (Future) Android application
...
```
