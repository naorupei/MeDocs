"""Times every key. Run: uv run python scripts/speed_test.py"""
import sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from openai import OpenAI
from app.config import EMBEDDING_MODEL, LLM_API_KEYS, LLM_BASE_URL, LLM_MODEL

print(f"Chat model: {LLM_MODEL} | Embedding model: {EMBEDDING_MODEL}\n")

for n, key in enumerate(LLM_API_KEYS, start=1):
    client = OpenAI(api_key=key, base_url=LLM_BASE_URL, max_retries=0, timeout=20)
    label = f"Key {n} (...{key[-4:]})"

    t = time.time()
    try:
        client.embeddings.create(model=EMBEDDING_MODEL, input="test")
        print(f"{label} embedding: {time.time() - t:.1f}s OK")
    except Exception as e:
        print(f"{label} embedding: FAILED after {time.time() - t:.1f}s -> {str(e)[:150]}")

    t = time.time()
    try:
        client.chat.completions.create(
            model=LLM_MODEL, max_tokens=20,
            messages=[{"role": "user", "content": "Say hello"}],
        )
        print(f"{label} chat:      {time.time() - t:.1f}s OK")
    except Exception as e:
        print(f"{label} chat:      FAILED after {time.time() - t:.1f}s -> {str(e)[:150]}")