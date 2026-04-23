# graph_workflow.py
# This file defines the LangGraph workflow
# It manages nodes, edges, state and routing logic

from langgraph.graph import StateGraph, END
from typing import TypedDict
from rag_pipeline import generate_answer
from hitl import escalate_to_human


# ── State Definition ─────────────────────────────────────
# This is the data object that flows between all nodes

class GraphState(TypedDict):
    query: str          # Original user query
    answer: str         # Generated answer
    confident: bool     # Whether answer is confident
    context: str        # Retrieved chunks
    escalated: bool     # Whether query was escalated
    final_response: str # Final message shown to user


# ── Node 1: Process Query ─────────────────────────────────
# Retrieves relevant chunks and generates an answer

def process_query_node(state: GraphState) -> GraphState:
    print("\n[NODE 1] Processing query...")

    # Call RAG pipeline
    result = generate_answer(state["query"])

    # Update state with results
    state["answer"] = result["answer"]
    state["confident"] = result["confident"]
    state["context"] = result["context"]
    state["escalated"] = False

    print(f"[NODE 1] Answer generated. Confident: {result['confident']}")

    return state


# ── Node 2: Generate Output ───────────────────────────────
# If confident → return answer directly to user

def output_node(state: GraphState) -> GraphState:
    print("\n[NODE 2] Preparing final response...")

    state["final_response"] = state["answer"]
    state["escalated"] = False

    print("[NODE 2] Response ready.")

    return state


# ── Node 3: Escalation Node ───────────────────────────────
# If not confident → escalate to human agent

def escalation_node(state: GraphState) -> GraphState:
    print("\n[NODE 3] Escalating to human agent...")

    # Determine reason for escalation
    reason = "Low confidence answer — query may be outside FAQ scope"

    # Call HITL module
    user_message = escalate_to_human(
        query=state["query"],
        reason=reason
    )

    state["final_response"] = user_message
    state["escalated"] = True

    return state


# ── Routing Function ──────────────────────────────────────
# Decides which node to go to after process_query_node

def route_query(state: GraphState) -> str:
    if state["confident"]:
        print("\n[ROUTER] Confident answer → routing to output node")
        return "output"
    else:
        print("\n[ROUTER] Low confidence → routing to escalation node")
        return "escalate"


# ── Build the Graph ───────────────────────────────────────

def build_graph():
    # Initialize graph with state
    graph = StateGraph(GraphState)

    # Add nodes
    graph.add_node("process_query", process_query_node)
    graph.add_node("output", output_node)
    graph.add_node("escalate", escalation_node)

    # Set entry point
    graph.set_entry_point("process_query")

    # Add conditional routing after process_query
    graph.add_conditional_edges(
        "process_query",
        route_query,
        {
            "output": "output",
            "escalate": "escalate"
        }
    )

    # Both output and escalate lead to END
    graph.add_edge("output", END)
    graph.add_edge("escalate", END)

    # Compile and return graph
    return graph.compile()


# ── Run the Graph ─────────────────────────────────────────

def run_graph(query: str) -> str:
    # Build graph
    app = build_graph()

    # Initial state
    initial_state = GraphState(
        query=query,
        answer="",
        confident=False,
        context="",
        escalated=False,
        final_response=""
    )

    # Run the graph
    final_state = app.invoke(initial_state)

    return final_state["final_response"]