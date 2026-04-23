# rag-cust-serv

RAG-based customer support assistant using Groq LLaMA3, LangGraph, and ChromaDB. Answers queries from a PDF knowledge base and escalates low-confidence responses to a human agent.

## Stack

- **LLM**: Groq LLaMA 3.1 8B Instant
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2`
- **Vector store**: ChromaDB
- **Orchestration**: LangGraph
- **Document loader**: LangChain + PyPDF

## Structure

```
app/
  main.py            # Entry point and chat loop
  ingest.py          # PDF ingestion and embedding pipeline
  rag_pipeline.py    # Retrieval and answer generation
  graph_workflow.py  # LangGraph nodes and routing logic
  hitl.py            # Human-in-the-loop escalation
docs/
  faq.pdf            # Source knowledge base
data/
  chroma_db/         # Persisted vector store
  escalation_log.json
```

## Setup

```bash
pip install -r requirements.txt
```

Add a `.env` file:

```
GROQ_API_KEY=your_key_here
```

Place your FAQ PDF at `docs/faq.pdf`.

## Usage

```bash
python main.py
```

**Commands during chat:**

| Command | Action |
|---|---|
| `quit` | Exit |
| `escalations` | View pending human escalations |
| `reingest` | Reload the PDF knowledge base |

## How it works

1. On first run, `ingest.py` loads `faq.pdf`, splits it into chunks, and stores embeddings in ChromaDB.
2. Each query goes through a LangGraph workflow: retrieve relevant chunks, generate an answer, and route based on confidence.
3. Confident answers are returned directly. Low-confidence answers are logged and escalated to a human agent with a 24-hour SLA.