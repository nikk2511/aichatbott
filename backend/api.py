import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from chromadb.config import Settings
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
from typing import List, Dict, Any, Optional
import json
from openai import OpenAI

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body schema
class AskRequest(BaseModel):
    query: str

class ComposeRequest(BaseModel):
    topic: str
    books: Optional[List[str]] = None  # optional list of specific book filenames to use

# ChromaDB setup
# Use absolute paths to avoid cwd-dependent bugs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PERSIST_DIR = os.path.join(BASE_DIR, "data", "chroma")
COLLECTION_NAME = "puja_books"

def get_chroma_client():
    """Get or create ChromaDB client and collection."""
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR, settings=Settings())
    collection = client.get_or_create_collection(COLLECTION_NAME)
    return collection

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """Split text into chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return splitter.split_text(text)

def read_books_text(only_books: List[str] = None) -> Dict[str, str]:
    """Read full text from PDFs under ./pdfs and return mapping of filename -> text.
    If only_books provided, restrict to those filenames.
    """
    pdf_dir = os.path.join(BASE_DIR, "pdfs")
    texts: Dict[str, str] = {}
    if not os.path.isdir(pdf_dir):
        return texts

    for filename in os.listdir(pdf_dir):
        if not filename.lower().endswith(".pdf"):
            continue
        if only_books and filename not in set(only_books):
            continue
        pdf_path = os.path.join(pdf_dir, filename)
        content = extract_text_from_pdf(pdf_path)
        if content:
            texts[filename] = content
    return texts

def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment")
    return OpenAI(api_key=api_key)

SYSTEM_FMT_INSTRUCTIONS = (
    "You are an expert Hindu priest and editor. You will receive raw excerpts from authentic puja books. "
    "Rewrite them into a crystal-clear, beginner-friendly guide in polished natural language. "
    "Output must be comprehensive and practical."
)

CHUNK_PROMPT = (
    "From the provided raw book excerpt, extract and normalize structured items. "
    "Return JSON with keys: materials (array of objects with name and why), steps (array of strings in order), "
    "timings (array of strings), dos (array), donts (array), mantras (array of objects with text and meaning), notes (array). "
    "Be faithful to the source; do not invent."
)

FINAL_PROMPT = (
    "You will receive a merged JSON draft compiled from multiple authentic books for the topic. "
    "Carefully deduplicate, resolve conflicts conservatively, and produce a final, polished guide in the following format:\n\n"
    "Materials (with simple explanations)\n"
    "1) ...\n"
    "\nProcedure (step-by-step)\n"
    "1) ...\n"
    "\nAdditional Notes\n- Best timing\n- Do's & Don'ts\n- Meanings of important mantras\n\n"
    "Write naturally as if inside the ChatGPT app. Keep it clear and beginner-friendly."
)

def compose_from_books(topic: str, only_books: List[str] = None) -> Dict[str, str]:
    """Compose a polished guide using OpenAI by reading book texts, chunking, summarizing, then finalizing."""
    # 1) Read books
    book_texts = read_books_text(only_books)
    if not book_texts:
        return {"content_markdown": "No books found to compose the guide."}

    client = get_openai_client()

    # 2) Per-book chunking and extraction
    aggregated: Dict[str, Any] = {
        "materials": [],
        "steps": [],
        "timings": [],
        "dos": [],
        "donts": [],
        "mantras": [],
        "notes": [],
        "sources": [],
    }

    splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300)

    # Hard limits to keep requests responsive
    max_books_to_process = int(os.getenv("COMPOSE_MAX_BOOKS", "3"))
    max_chunks_per_book = int(os.getenv("COMPOSE_MAX_CHUNKS_PER_BOOK", "3"))
    max_total_chunks = int(os.getenv("COMPOSE_MAX_TOTAL_CHUNKS", "8"))
    processed_total_chunks = 0

    for book_index, (filename, text) in enumerate(book_texts.items()):
        if book_index >= max_books_to_process:
            break
        chunks_all = splitter.split_text(text)
        # Take only the first N reasonably sized chunks per book
        chunks = chunks_all[:max_chunks_per_book]
        for idx, chunk in enumerate(chunks):
            if processed_total_chunks >= max_total_chunks:
                break
            # Guard against extremely small or whitespace-only chunks
            if len(chunk.strip()) < 100:
                continue
            try:
                resp = client.chat.completions.create(
                    model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
                    temperature=0.2,
                    timeout=60,
                    messages=[
                        {"role": "system", "content": SYSTEM_FMT_INSTRUCTIONS},
                        {
                            "role": "user",
                            "content": (
                                f"Topic: {topic}\n\n"
                                f"Source Book: {filename} (chunk {idx+1}/{len(chunks)})\n\n"
                                f"Raw Excerpt:\n" + chunk + "\n\n" + CHUNK_PROMPT
                            ),
                        },
                    ],
                )
                content = resp.choices[0].message.content or "{}"
                # Try to parse JSON from the message. If it contains text + JSON, extract JSON block
                import json as _json
                json_str = content
                # crude extraction of a JSON object
                if "{" in content and "}" in content:
                    start = content.find("{")
                    end = content.rfind("}")
                    json_str = content[start : end + 1]
                data = _json.loads(json_str)
            except Exception:
                continue

            # Merge
            for key in ["materials", "steps", "timings", "dos", "donts", "mantras", "notes"]:
                if key in data and isinstance(data[key], list):
                    aggregated[key].extend(data[key])
            aggregated["sources"].append({"book": filename, "chunk_index": idx})
            processed_total_chunks += 1

    # 3) Final polishing pass
    try:
        final_resp = client.chat.completions.create(
            model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
            temperature=0.3,
            timeout=60,
            messages=[
                {"role": "system", "content": SYSTEM_FMT_INSTRUCTIONS},
                {
                    "role": "user",
                    "content": (
                        f"Compose a final, polished guide for: {topic}\n\n"
                        f"Here is the merged JSON draft from authentic books:\n\n{json.dumps(aggregated)}\n\n"
                        + FINAL_PROMPT
                    ),
                },
            ],
        )
        final_text = final_resp.choices[0].message.content or ""
    except Exception as e:
        final_text = f"Error finalizing guide: {e}"

    return {"content_markdown": final_text}

def ingest_pdfs():
    """Ingest PDF files into ChromaDB."""
    collection = get_chroma_client()
    
    # Check if collection is empty
    if collection.count() > 0:
        print(f"Collection already has {collection.count()} documents")
        return
    
    pdf_dir = os.path.join(BASE_DIR, "pdfs")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    
    total_chunks = 0
    for filename in os.listdir(pdf_dir):
        if not filename.endswith(".pdf"):
            continue
            
        pdf_path = os.path.join(pdf_dir, filename)
        print(f"Processing {filename}...")
        
        text = extract_text_from_pdf(pdf_path)
        if text:
            chunks = splitter.split_text(text)
            
            for i, chunk in enumerate(chunks):
                # Clean the chunk
                chunk = re.sub(r'\s+', ' ', chunk).strip()
                if len(chunk) < 50:  # Skip very short chunks
                    continue
                    
                collection.add(
                    documents=[chunk],
                    metadatas=[{
                        "book_title": filename,
                        "page": i,
                        "chunk_id": f"{filename}_{i}"
                    }],
                    ids=[f"{filename}_{i}"]
                )
            total_chunks += len(chunks)
            print(f"Added {len(chunks)} chunks from {filename}")
    
    print(f"Ingestion complete. Total chunks: {total_chunks}")

def search_books(query: str, n_results: int = 5) -> List[Dict[str, Any]]:
    """Search through the books for relevant information."""
    collection = get_chroma_client()
    
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        search_results = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                search_results.append({
                    "content": doc,
                    "book": results['metadatas'][0][i]['book_title'],
                    "page": results['metadatas'][0][i]['page'],
                    "relevance_score": 1 - results['distances'][0][i] if results['distances'] else 0
                })
        
        return search_results
    except Exception as e:
        print(f"Error searching books: {e}")
        return []

def create_structured_response(query: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a structured response based on search results."""
    if not search_results:
        return {
            "summary": f"Information about {query} was not found in the available books.",
            "steps": [],
            "materials": [],
            "timings": [],
            "mantras": [],
            "sources": [],
            "notes": "Please check the spelling or try a different query. The available books contain information about Sai Divya Pooja, Siva Puranam, Lakshmi Puja, Chandi, and Durga Puja."
        }
    
    # Extract relevant information from search results
    all_content = " ".join([result["content"] for result in search_results])
    
    # Create summary
    summary = f"Information about {query} based on authentic texts: {all_content[:300]}..."
    
    # Extract steps (look for numbered lists, bullet points, etc.)
    steps = []
    step_patterns = [
        r'(\d+\.\s*[^.]*\.)',
        r'(step\s*\d+[^.]*\.)',
        r'(first[^.]*\.)',
        r'(second[^.]*\.)',
        r'(third[^.]*\.)',
        r'(then[^.]*\.)',
        r'(next[^.]*\.)',
        r'(after[^.]*\.)'
    ]
    
    for pattern in step_patterns:
        matches = re.findall(pattern, all_content, re.IGNORECASE)
        for match in matches[:5]:  # Limit to 5 steps
            steps.append({
                "title": f"Step {len(steps) + 1}",
                "instruction": match.strip()
            })
    
    # Extract materials (look for common puja items)
    materials = []
    material_keywords = [
        "incense", "flowers", "coconut", "banana", "ghee", "kumkum", "chandan",
        "kalash", "diya", "camphor", "sweets", "fruits", "rice", "water",
        "mango leaves", "tulsi", "betel leaves", "betel nuts"
    ]
    
    for keyword in material_keywords:
        if keyword.lower() in all_content.lower():
            materials.append({
                "name": keyword.title(),
                "product_match": "https://www.amazon.in"
            })
    
    # Extract timings
    timings = []
    timing_patterns = [
        r'(morning[^.]*\.)',
        r'(evening[^.]*\.)',
        r'(sunrise[^.]*\.)',
        r'(sunset[^.]*\.)',
        r'(brahma muhurta[^.]*\.)',
        r'(amavasya[^.]*\.)',
        r'(purnima[^.]*\.)'
    ]
    
    for pattern in timing_patterns:
        matches = re.findall(pattern, all_content, re.IGNORECASE)
        for match in matches:
            timings.append(match.strip())
    
    # Extract mantras (look for Sanskrit text)
    mantras = []
    mantra_patterns = [
        r'(ॐ[^।]*।)',
        r'(om[^.]*\.)',
        r'(namah[^.]*\.)',
        r'(swaha[^.]*\.)'
    ]
    
    for pattern in mantra_patterns:
        matches = re.findall(pattern, all_content, re.IGNORECASE)
        for match in matches:
            mantras.append(match.strip())
    
    # Create sources list
    sources = []
    for result in search_results[:3]:  # Top 3 sources
        sources.append({
            "book": result["book"],
            "page": result["page"],
            "snippet": result["content"][:200] + "..."
        })
    
    return {
        "summary": summary,
        "steps": steps,
        "materials": materials,
        "timings": timings,
        "mantras": mantras,
        "sources": sources,
        "notes": f"This information is extracted from authentic texts: {', '.join(set([r['book'] for r in search_results]))}. Please consult with learned priests for proper guidance."
    }

# Test route
@app.get("/")
def root():
    return {"message": "RAG Puja AI API is running! (Using your uploaded books)"}

# Chat endpoint
@app.post("/api/ask")
def ask_question(request: AskRequest):
    try:
        # First, ensure books are ingested
        ingest_pdfs()
        
        # Search through the books
        search_results = search_books(request.query, n_results=5)
        
        # Create structured response
        response = create_structured_response(request.query, search_results)
        
        return response

    except Exception as e:
        return {
            "summary": "Error occurred while processing your request",
            "steps": [],
            "materials": [],
            "timings": [],
            "mantras": [],
            "sources": [],
            "notes": f"Error: {str(e)}. Please try again."
        }

# Health check endpoint
@app.get("/health")
def health_check():
    collection = get_chroma_client()
    return {
        "status": "healthy",
        "documents_count": collection.count(),
        "message": "RAG system is ready"
    }

# Compose endpoint: reads all books, calls ChatGPT, returns polished guide
@app.post("/api/compose")
def compose_endpoint(payload: ComposeRequest):
    try:
        result = compose_from_books(topic=payload.topic, only_books=payload.books)
        # Return a uniform structure for the frontend
        return {
            "summary": None,
            "steps": [],
            "materials": [],
            "timings": [],
            "mantras": [],
            "sources": [],
            "notes": None,
            "content_markdown": result.get("content_markdown", "")
        }
    except Exception as e:
        return {
            "summary": "Error composing guide",
            "steps": [],
            "materials": [],
            "timings": [],
            "mantras": [],
            "sources": [],
            "notes": f"Error: {str(e)}",
            "content_markdown": ""
        }
