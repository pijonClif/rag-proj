# main.py
# This is the main entry point of the application
# Run this file to start the customer support assistant

import os
from ingest import ingest_document
from graph_workflow import run_graph
from hitl import view_pending_escalations

# ── Welcome Banner ────────────────────────────────────────

def print_banner():
    print("\n" + "="*55)
    print("   RAG-Based Customer Support Assistant")
    print("   Powered by Groq LLaMA3 + LangGraph + ChromaDB")
    print("="*55)


# ── Check if knowledge base exists ───────────────────────

def check_knowledge_base():
    if not os.path.exists("./data/chroma_db"):
        print("\n[SETUP] Knowledge base not found.")
        print("[SETUP] Running ingestion pipeline first...")
        ingest_document()
        print("[SETUP] Knowledge base created successfully!\n")
    else:
        print("\n[SETUP] Knowledge base found. Ready to go!\n")


# ── Main Chat Loop ────────────────────────────────────────

def main():
    print_banner()

    # Step 1: Make sure knowledge base is ready
    check_knowledge_base()

    print("Type your question below.")
    print("Commands:")
    print("  'quit'       → Exit the assistant")
    print("  'escalations' → View pending escalations")
    print("  'reingest'   → Reload the PDF knowledge base")
    print("-"*55)

    # Step 2: Start chat loop
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()

        # Skip empty input
        if not user_input:
            continue

        # Exit command
        if user_input.lower() == "quit":
            print("\nThank you for using the support assistant. Goodbye!")
            break

        # View escalations command
        elif user_input.lower() == "escalations":
            view_pending_escalations()

        # Reingest command
        elif user_input.lower() == "reingest":
            print("\n[SETUP] Reingesting knowledge base...")
            ingest_document()
            print("[SETUP] Knowledge base updated!")

        # Normal query
        else:
            print("\nAssistant: Searching knowledge base...")
            response = run_graph(user_input)
            print(f"\nAssistant: {response}")
            print("-"*55)


# ── Entry Point ───────────────────────────────────────────

if __name__ == "__main__":
    main()