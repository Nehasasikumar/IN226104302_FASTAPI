from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import math

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

def chunk_text(text, chunk_size=2000, overlap=200):
    chunks = []
    start = 0
    L = len(text)
    idx = 0
    while start < L:
        end = min(start + chunk_size, L)
        chunk = text[start:end]
        chunks.append({"id": idx, "text": chunk, "start": start, "end": end})
        idx += 1
        if end == L:
            break
        start = end - overlap
    return chunks

def ingest_pdf(file_stream, doc_id: str = "document"):
    reader = PdfReader(file_stream)
    text = "\n".join([p.extract_text() or "" for p in reader.pages])

    chunks = chunk_text(text)

    model = SentenceTransformer(EMBED_MODEL_NAME)
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True)

    client = chromadb.Client()
    collection = None
    try:
        collection = client.get_collection(name="rag_docs")
    except Exception:
        collection = client.create_collection(name="rag_docs")

    ids = [f"{doc_id}-{c['id']}" for c in chunks]
    metadatas = [{"doc_id": doc_id, "start": c["start"], "end": c["end"]} for c in chunks]
    documents = texts

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings.tolist(),
    )

    return {"doc_id": doc_id, "chunks": len(chunks)}
