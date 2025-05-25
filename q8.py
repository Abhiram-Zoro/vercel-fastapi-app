import os
# from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import Dict, List
import numpy as np
import traceback

# Load environment variables from .env file
# load_dotenv()

# Ensure AIPROXY_TOKEN is properly loaded
AIPROXY_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIxZjMwMDIxNThAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.OBG8YpRtQ-Y1X84pAm7esKxtX3x-GZPyhgh0hpsuLQU"
if not AIPROXY_TOKEN:
    raise ValueError("AIPROXY_TOKEN environment variable not set. Make sure it's defined in your .env file.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def cosine_similarity(a, b):
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return 0.0 if norm_a == 0 or norm_b == 0 else np.dot(a, b) / (norm_a * norm_b)

@app.post("/similarity")
async def get_similar_docs(request: Request, request_body: Dict):
    try:
        docs: List[str] = request_body.get("docs")
        query: str = request_body.get("query")

        if not docs or not query:
            raise HTTPException(status_code=400, detail="Missing 'docs' or 'query' in request body")

        input_texts = [query] + docs  # Combine query and docs for embeddings request

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AIPROXY_TOKEN}"
        }
        data = {"model": "text-embedding-3-small", "input": input_texts}
        embeddings_response = requests.post(
            "https://aiproxy.sanand.workers.dev/openai/v1/embeddings",
            headers=headers,
            json=data
        )

        embeddings_response.raise_for_status()
        embeddings_data = embeddings_response.json()

        query_embedding = embeddings_data['data'][0]['embedding']
        doc_embeddings = [emb['embedding'] for emb in embeddings_data['data'][1:]]

        similarities = [(i, cosine_similarity(query_embedding, doc_embeddings[i]), docs[i]) for i in range(len(docs))]
        ranked_docs = sorted(similarities, key=lambda x: x[1], reverse=True)
        top_matches = [doc for _, _, doc in ranked_docs[:min(3, len(ranked_docs))]]

        return {"matches": top_matches}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with AI Proxy: {e}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "_main_":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)