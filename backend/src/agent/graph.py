# backend/src/agent/graph.py
from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes.planner import planner_node
from .nodes.search import search_node
from .nodes.filter import filter_node

# 1. Initialize the Graph with our State schema
workflow = StateGraph(AgentState)

# 2. Add the Nodes (The Workers)
workflow.add_node("planner", planner_node)
workflow.add_node("search", search_node)
workflow.add_node("filter", filter_node)

# 3. Define the Edges (The Assembly Line)
# Start -> Planner
workflow.set_entry_point("planner")

# Planner -> Search
workflow.add_edge("planner", "search")

# Search -> Filter
workflow.add_edge("search", "filter")

# Filter -> End
workflow.add_edge("filter", END)

# 4. Compile the Graph
# This creates the executable "brain" we can invoke
graph = workflow.compile()