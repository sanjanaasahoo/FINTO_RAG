from sentence_transformers import SentenceTransformer
import faiss
import pickle
from groq import Groq
from tavily import TavilyClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index and metadata

index = faiss.read_index("../FINTO_RAG/vector_store/faiss_index.bin")

with open("../FINTO_RAG/vector_store/metadata.pkl", "rb")as f:
    metadata = pickle.load(f)

# Initialize clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Threshold
LOCAL_CONFIDENCE_THRESHOLD = 0.4


# ======================
# LOCAL SEARCH
# ======================
def search_local(query, k=3):
    query_vector = model.encode([query]).astype("float32")
    faiss.normalize_L2(query_vector)
    D, I = index.search(query_vector, k)

    results = []
    for i in range(k):
        results.append(metadata[I[0][i]]["text"])

    top_score = float(D[0][0])
    return results, top_score


# ======================
# WEB SEARCH (TAVILY)
# ======================
def search_web(query):
    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=3,
        include_answer=True
    )

    chunks = []

    if response.get("answer"):
        chunks.append(f"[Web Summary]: {response['answer']}")

    for result in response.get("results", []):
        if result.get("content"):
            chunks.append(f"[Source: {result.get('url', 'web')}]\n{result['content']}")

    return chunks


# ======================
# MAIN RAG PIPELINE
# ======================
def rag_pipeline(query):
    local_chunks, score = search_local(query)

    if score >= LOCAL_CONFIDENCE_THRESHOLD:
        context = "\n".join(local_chunks)
    else:
        web_chunks = search_web(query)
        context = "\n".join(web_chunks)

    prompt = f"""
    Answer based on context:
    {context}

    Question: {query}
    """

    response = groq_client.chat.completions.create(
       model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content