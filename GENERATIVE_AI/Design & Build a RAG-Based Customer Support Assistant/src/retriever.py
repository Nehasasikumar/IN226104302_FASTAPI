from sentence_transformers import SentenceTransformer
import chromadb

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

def retrieve(query: str, top_k: int = 5):
    model = SentenceTransformer(EMBED_MODEL_NAME)
    q_emb = model.encode([query], convert_to_numpy=True)[0].tolist()

    client = chromadb.Client()
    try:
        collection = client.get_collection(name="rag_docs")
    except Exception:
        return []

    results = collection.query(
        query_embeddings=[q_emb],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    # results structure: dict with 'documents','metadatas','distances'
    hits = []
    docs = results.get("documents", [])[0]
    metas = results.get("metadatas", [])[0]
    dists = results.get("distances", [])[0]
    for doc, meta, dist in zip(docs, metas, dists):
        hits.append({"text": doc, "metadata": meta, "score": 1 - dist})
    return hits
