# RAG-Based Customer Support Assistant

This project is a Retrieval-Augmented Generation (RAG) based customer support system built using LangGraph and Human-in-the-Loop (HITL).

## 🚀 Features

- Processes FAQ PDF documents
- Stores embeddings using ChromaDB
- Retrieves relevant information for user queries
- Generates context-aware responses using LLM (Groq LLaMA 3.1)
- Uses LangGraph for decision-based workflow
- Escalates low-confidence queries to human support (HITL)

## 🧠 Tech Stack

- Python
- LangChain
- LangGraph
- ChromaDB
- Groq API

## 📂 Project Structure
```
RAG_System_Project/
├── ingest.py
├── rag_pipeline.py
├── graph_workflow.py
├── hitl.py
├── faq.pdf
├── main.py
```
---

## ▶️ How to Run

1. Install dependencies:
   ```
   pip install langchain langchain-community langchain-groq
   pip install langchain-huggingface langchain-chroma
   pip install chromadb sentence-transformers pypdf langgraph
   ```
2. Create a Virtual Environment
   ```
   python -m venv rag_env

   # Windows
   rag_env\Scripts\activate

   # Mac/Linux
   source rag_env/bin/activate
   ```
3. Add Your Groq API Key
Open rag_pipeline.py and replace:
   ```
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
4. Add Your FAQ PDF
Place your FAQ document in the project folder and name it:
  ```
  faq.pdf
  ```
5. Running the Project:
   ```
   python main.py
   ```
On first run, the system will automatically ingest the PDF and build the knowledge base.

---
   
## 🔀 LangGraph Workflow
```

[START]
   ↓
[Input: User Query]
   ↓
[Node 1: Process Query]
(Retrieve relevant chunks + Generate answer using LLM)
   ↓
[Decision: Is response confident?]
   ↓                      ↓
[Yes]                    [No]
   ↓                      ↓
[Node 2: Output]        [Node 3: Escalate (HITL)]
(Return answer)         (Log query + Notify human)
   ↓                      ↓
[END]                  [END]
```
---

## 👤 HITL Escalation
When the system cannot answer confidently it:

1. 🚨 Logs the query with timestamp and reason
2. 📋 Saves it to escalation_log.json
3. 🔔 Notifies a human agent in the terminal
4. 💬 Returns an escalation ID to the user

To view all pending escalations:
```
You: escalations
```
---

👩‍💻 Author
Samruddhi Khedkar
Agentic AI Intern — Innomatics Research Labs
BTech Electronics & Telecommunication Engineering
