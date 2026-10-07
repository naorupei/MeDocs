from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.rag import answer_question
from app.schemas import ChatRequest, ChatResponse, IngestRequest
from app.store import store

app = FastAPI(title="MediLens AI Backend")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/health")
def health():
    docs = {c["document"] for c in store.chunks}
    return {"status": "ok", "chunks": len(store.chunks), "documents": sorted(docs)}


@app.post("/ingest")
def ingest(req: IngestRequest):
    """Called by Member 2's document processor."""
    try:
        count = store.add_chunks([c.model_dump() for c in req.chunks])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingest failed: {e}")
    return {"ingested": count, "total_chunks": len(store.chunks)}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is empty.")
    try:
        return answer_question(question)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI backend error: {e}")


@app.delete("/reset")
def reset():
    store.clear()
    return {"status": "cleared"}