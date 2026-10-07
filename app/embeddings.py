import numpy as np

from app.config import EMBEDDING_MODEL, EMBEDDING_PROVIDER
from app.llm import embed_via_api

_local_model = None


def _get_local_model():
    global _local_model
    if _local_model is None:
        from fastembed import TextEmbedding
        _local_model = TextEmbedding(model_name=EMBEDDING_MODEL)
    return _local_model


def _normalize(vectors) -> np.ndarray:
    """Make every vector length 1, so dot product == cosine similarity."""
    arr = np.asarray(vectors, dtype=np.float32)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    return arr / np.maximum(norms, 1e-12)


def embed_texts(texts: list[str]) -> np.ndarray:
    """Embed document chunks. Returns array of shape (len(texts), dim)."""
    if EMBEDDING_PROVIDER == "openai":
        vectors = []
        for i in range(0, len(texts), 100):
            vectors.extend(embed_via_api(EMBEDDING_MODEL, texts[i:i + 100]))
    else:
        vectors = list(_get_local_model().embed(texts))
    return _normalize(vectors)


def embed_query(question: str) -> np.ndarray:
    """Embed a question. Returns array of shape (dim,)."""
    if EMBEDDING_PROVIDER == "openai":
        return embed_texts([question])[0]
    vectors = list(_get_local_model().query_embed([question]))
    return _normalize(vectors)[0]