import os
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.config import Settings
from uuid import uuid4

CHROMA_PERSIST_DIR = "./data/chroma"
COLLECTION_NAME = "puja_books"

def ingest_pdfs(pdf_dir: str):
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR, settings=Settings())
    collection = client.get_or_create_collection(COLLECTION_NAME)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    total_chunks = 0
    for filename in os.listdir(pdf_dir):
        if not filename.endswith(".pdf"):
            continue
        path = os.path.join(pdf_dir, filename)
        print(f"Processing {path}...")
        with pdfplumber.open(path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            chunks = splitter.split_text(text)
            for i, chunk in enumerate(chunks):
                collection.add(
                    documents=[chunk],
                    metadatas=[{
                        "book_title": filename,
                        "page": i,
                        "chunk_id": str(uuid4())
                    }],
                    ids=[str(uuid4())]
                )
            total_chunks += len(chunks)

    print(f"Ingestion complete. Total chunks: {total_chunks}")

if __name__ == "__main__":
    ingest_pdfs("./pdfs")
