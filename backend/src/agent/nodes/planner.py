# backend/src/agent/nodes/planner.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from ..state import AgentState, SearchPlan
import os

# 1. Initialize Gemini 3 Pro (The "Brain")
# We use temperature=0 for strict plan adherence
llm = ChatGoogleGenerativeAI(
    model="gemini-3-pro-preview",
    temperature=0,
    google_api_key=os.environ["GOOGLE_API_KEY"]
)

# 2. The Prompt
PLANNER_PROMPT = """You are a Shopping Assistant Planner.
Your job is to break down a user's vague request into a precise search strategy.

User Request: {user_query}

Guidelines:
1. Generate 3-5 distinct search queries to maximize coverage.
2. Extract specific constraints (max price, must-have features).
3. Identify negative keywords to filter noise.
4. **CRITICAL**: Generate queries that are highly specific and target individual product pages, not search result pages.
    - GOOD: "buy Keychron Q1 v2 mechanical keyboard", "Apple Macbook Pro 16 inch M3 price"
    - BAD: "mechanical keyboards", "laptops site:bestbuy.com"
5. Generate queries that target product websites, and NOT reviews. Your queries should use "site:amazon.com", "site:bestbuy.com", "buy [item] online", etc.

Return the result strictly as a structured SearchPlan."""

# 3. The Node Function
def planner_node(state: AgentState):
    print("--- PLANNER NODE (Gemini 3): Generating search strategy ---")
    user_query = state['original_query']

    # Gemini supports .with_structured_output() natively now
    structured_llm = llm.with_structured_output(SearchPlan)
    
    plan = structured_llm.invoke([
        SystemMessage(content=PLANNER_PROMPT.format(user_query=user_query)),
        HumanMessage(content="Analyze this request.")
    ])

    return {"search_plan": plan}