import json

import numpy as np

from app.config import DATA_DIR, MAX_PER_DOC, TOP_K
from app.embeddings import embed_query, embed_texts

CHUNKS_FILE = DATA_DIR / "chunks.json"
VECTORS_FILE = DATA_DIR / "vectors.npy"


class VectorStore:
    """In-memory vector store, saved to disk after every change."""

    def __init__(self):
        self.chunks: list[dict] = []
        self.vectors = np.zeros((0, 0), dtype=np.float32)
        self._load()

    # ---------- persistence ----------
    def _load(self):
        if CHUNKS_FILE.exists() and VECTORS_FILE.exists():
            self.chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
            self.vectors = np.load(VECTORS_FILE)

    def _save(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        CHUNKS_FILE.write_text(json.dumps(self.chunks, ensure_ascii=False), encoding="utf-8")
        np.save(VECTORS_FILE, self.vectors)

    # ---------- adding data ----------
    def add_chunks(self, new_chunks: list[dict]) -> int:
        """Add chunks (Member 2's format). Re-ingesting a document_id replaces it."""
        clean = []
        for c in new_chunks:
            text = (c.get("text") or "").strip()
            if not text:
                continue
            clean.append({
                "text": text,
                "document_id": str(c["document_id"]),
                "document": c["document"],
                "page": int(c["page"]),
                "section": c.get("section") or "",
            })
        if not clean:
            return 0

        # Drop old chunks of the same documents
        replaced_ids = {c["document_id"] for c in clean}
        keep = [i for i, c in enumerate(self.chunks) if c["document_id"] not in replaced_ids]
        self.chunks = [self.chunks[i] for i in keep]
        if self.vectors.shape[0] > 0:
            self.vectors = self.vectors[np.array(keep, dtype=int)]

        # Embed with document + section name included, so "January" / "Lab Results" help retrieval
        texts = [f"{c['document']} | {c['section']}\n{c['text']}" for c in clean]
        new_vectors = embed_texts(texts)

        if self.vectors.shape[0] == 0:
            self.vectors = new_vectors
        else:
            self.vectors = np.vstack([self.vectors, new_vectors])
        self.chunks.extend(clean)
        self._save()
        return len(clean)

    def clear(self):
        self.chunks = []
        self.vectors = np.zeros((0, 0), dtype=np.float32)
        self._save()

    # ---------- retrieval ----------
    def search(self, question: str, top_k: int = TOP_K, max_per_doc: int = MAX_PER_DOC) -> list[dict]:
        """Return the best chunks, capped per document so cross-document
        questions get evidence from several documents."""
        if not self.chunks:
            return []

        scores = self.vectors @ embed_query(question)
        results = []
        per_doc_count: dict[str, int] = {}

        for i in np.argsort(-scores):
            chunk = self.chunks[i]
            doc_id = chunk["document_id"]
            if per_doc_count.get(doc_id, 0) >= max_per_doc:
                continue
            per_doc_count[doc_id] = per_doc_count.get(doc_id, 0) + 1
            results.append({**chunk, "score": float(scores[i])})
            if len(results) >= top_k:
                break
        return results


store = VectorStore()  # one shared instance