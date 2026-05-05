import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# ---------- CONFIG ----------
DATA_DIR = "../data/raw_txt_definitions"   # adjust if your texts are elsewhere
OUT_DIR = "../vector_store"
CHUNK_SIZE = 400
CHUNK_OVERLAP = 50

# ---------- LOAD TEXT FILES ----------
def load_texts(folder):
    texts = []
    for fname in os.listdir(folder):
        if fname.endswith(".txt"):
            with open(os.path.join(folder, fname), "r", encoding="utf-8") as f:
                texts.append(f.read())
    return texts

# ---------- SIMPLE CHUNKING ----------
def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap
    return chunks

# ---------- BUILD INDEX ----------
def main():
    print("Loading data...")
    docs = load_texts(DATA_DIR)

    print("Chunking...")
    chunks = []
    for d in docs:
        chunks.extend(chunk_text(d))

    print(f"Total chunks: {len(chunks)}")

    print("Embedding...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks, convert_to_numpy=True)

    # normalize for cosine similarity with inner product
    faiss.normalize_L2(embeddings)

    print("Creating FAISS index...")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    # ensure output dir exists
    os.makedirs(OUT_DIR, exist_ok=True)

    print("Saving index + metadata...")
    faiss.write_index(index, os.path.join(OUT_DIR, "faiss_index.bin"))

    metadata = [{"text": c} for c in chunks]
    with open(os.path.join(OUT_DIR, "metadata.pkl"), "wb") as f:
        pickle.dump(metadata, f)

    print("✅ Done! Vector store created.")

if __name__ == "__main__":
    main()