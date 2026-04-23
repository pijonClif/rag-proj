# rag_pipeline.py - FIXED VERSION

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os

from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

CHROMA_PATH = "./data/chroma_db"

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",
    temperature=0.2,
    max_tokens=512
)

PROMPT_TEMPLATE = """You are a helpful customer support assistant.
Answer using ONLY the context below.
If the answer is not in the context, say exactly:
"I don't have enough information to answer this question."

Context:
{context}

Question: {question}

Answer:"""


def get_retriever():
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )
    return vectorstore.as_retriever(search_kwargs={"k": 3})


def generate_answer(query: str) -> dict:
    print(f"\nProcessing query: {query}")

    retriever = get_retriever()
    relevant_chunks = retriever.invoke(query)

    if not relevant_chunks:
        return {
            "query": query,
            "answer": "I don't have enough information to answer this question.",
            "confident": False,
            "context": ""
        }

    # Limit context to avoid token overflow
    context = "\n\n".join([
        chunk.page_content[:300]
        for chunk in relevant_chunks
    ])

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | llm

    try:
        response = chain.invoke({
            "context": context,
            "question": query
        })
        answer = response.content

    except Exception as e:
        print(f"[ERROR] LLM call failed: {e}")
        return {
            "query": query,
            "answer": "I don't have enough information to answer this question.",
            "confident": False,
            "context": context
        }

    not_confident_phrases = [
        "i don't have enough information",
        "i cannot answer",
        "not found in the context",
        "i don't know"
    ]

    confident = not any(
        phrase in answer.lower()
        for phrase in not_confident_phrases
    )

    return {
        "query": query,
        "answer": answer,
        "confident": confident,
        "context": context
    }