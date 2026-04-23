# ingest.py
# This file loads the FAQ PDF, splits it into chunks,
# creates embeddings and stores them in ChromaDB

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

# Path to your FAQ PDF
PDF_PATH = "./docs/faq.pdf"

# ChromaDB storage folder
CHROMA_PATH = "./data/chroma_db"

def ingest_document():
    print("Loading PDF...")
    
    # Step 1: Load the PDF
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"Loaded {len(documents)} page(s) from PDF")

    # Step 2: Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    # Step 3: Load HuggingFace embedding model
    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # Step 4: Store chunks + embeddings in ChromaDB
    print("Storing embeddings in ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    
    print("Ingestion complete! Knowledge base is ready.")
    return vectorstore

if __name__ == "__main__":
    ingest_document()