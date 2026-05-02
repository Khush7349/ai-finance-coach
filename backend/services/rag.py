from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
model = SentenceTransformer("all-MiniLM-L6-v2")
index = None
metadata_store = []
def build_index(df):
    global index, metadata_store
    if df is None or df.empty:
        index = None
        metadata_store = []
        return
    metadata_store = []
    texts = []
    for _, row in df.iterrows():
        text = (
            f"On {row['date']}, spent {row['amount']} "
            f"on {row['category']} at {row.get('merchant','unknown')} "
            f"via {row.get('type','unknown')}"
        )
        texts.append(text)
        metadata_store.append({
            "text": text,
            "date": str(row["date"]),
            "amount": row["amount"],
            "category": row["category"],
            "merchant": row.get("merchant"),
            "type": row.get("type")
        })
    embeddings = model.encode(texts, batch_size=32)
    embeddings = np.array(embeddings).astype("float32")
    faiss.normalize_L2(embeddings)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  
    index.add(embeddings)
def query_rag(query, k=5):
    if index is None or len(metadata_store) == 0:
        return []
    query_vec = model.encode([query]).astype("float32")
    faiss.normalize_L2(query_vec)
    scores, indices = index.search(query_vec, k)
    results = []
    for idx in indices[0]:
        if idx < len(metadata_store):
            results.append(metadata_store[idx])
    return results