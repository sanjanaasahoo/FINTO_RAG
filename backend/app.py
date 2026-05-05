import sys
import os

sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline import rag_pipeline

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask_question(request: QueryRequest):
    try:
        answer = rag_pipeline(request.query)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
    

    chunks = []

    if response.get("answer"):
        chunks.append(f"[Web Summary]: {response['answer']}")

    for result in response.get("results", []):
        if result.get("content"):
            chunks.append(f"[Source: {result.get('url', 'web')}]\n{result['content']}")

    return chunks