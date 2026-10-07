import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# LLM: one or more keys, comma-separated
_raw_keys = os.getenv("LLM_API_KEYS") or os.getenv("LLM_API_KEY", "")
LLM_API_KEYS = [k.strip() for k in _raw_keys.split(",") if k.strip()]
LLM_BASE_URL = os.getenv("LLM_BASE_URL") or None
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-flash-lite-latest")
LLM_MODELS = [m.strip() for m in os.getenv("LLM_MODELS", LLM_MODEL).split(",") if m.strip()]

# Embeddings
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai")  # "local" or "openai"
_default_embedding_model = (
    "text-embedding-3-small" if EMBEDDING_PROVIDER == "openai" else "BAAI/bge-small-en-v1.5"
)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", _default_embedding_model)

# Retrieval
TOP_K = int(os.getenv("TOP_K", "8"))
MAX_PER_DOC = int(os.getenv("MAX_PER_DOC", "3"))
MIN_SCORE = float(os.getenv("MIN_SCORE", "0.2"))

# Where the index is saved (so a server restart doesn't lose it)
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

REFUSAL_ANSWER = "I cannot determine this from the provided documents."