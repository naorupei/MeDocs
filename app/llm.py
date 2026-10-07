import time

from openai import OpenAI, OpenAIError

from app.config import LLM_API_KEYS, LLM_BASE_URL, LLM_MODELS

_clients: list[OpenAI] = []
_next_index = 0


def _init_clients():
    if not LLM_API_KEYS:
        raise RuntimeError("No API key set. Add LLM_API_KEYS to your .env file.")
    if not _clients:
        for key in LLM_API_KEYS:
            _clients.append(OpenAI(api_key=key, base_url=LLM_BASE_URL, max_retries=0, timeout=15))


def get_client() -> OpenAI:
    """Return the next client in rotation (round-robin)."""
    global _next_index
    _init_clients()
    client = _clients[_next_index % len(_clients)]
    _next_index += 1
    return client


def ask_llm(system_prompt: str, user_prompt: str) -> str:
    """Try each model in turn (rotating keys). Two rounds before giving up."""
    _init_clients()
    last_error = None

    for _ in range(2):  # two rounds
        for model in LLM_MODELS:
            client = get_client()
            try:
                response = client.chat.completions.create(
                    model=model,
                    temperature=0,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                return response.choices[0].message.content or ""
            except OpenAIError as e:
                last_error = e
                print(f"[llm] {model} failed: {type(e).__name__}: {str(e)[:150]}")
        time.sleep(2)

    raise RuntimeError(f"All models failed. Last error: {last_error}")


def embed_via_api(model: str, texts: list[str]) -> list[list[float]]:
    """Create embeddings. If a key fails, try the next key."""
    _init_clients()
    last_error = None

    for _ in range(len(_clients)):
        client = get_client()
        try:
            resp = client.embeddings.create(model=model, input=texts)
            return [d.embedding for d in resp.data]
        except OpenAIError as e:
            last_error = e
            print(f"[embeddings] a key failed: {type(e).__name__}: {str(e)[:200]}")

    raise RuntimeError(f"All keys failed. Last error: {last_error}")