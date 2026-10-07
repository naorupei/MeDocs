import ast
import json
import operator

from app.config import MIN_SCORE, REFUSAL_ANSWER
from app.llm import ask_llm
from app.store import store

SYSTEM_PROMPT = """You are MediLens, an assistant that answers questions about medical documents.
You may use ONLY the numbered context excerpts given to you.

RULES:
1. Use only facts explicitly written in the excerpts. Never use outside knowledge. Never guess.
2. If the excerpts do not contain enough information, set "answerable" to false.
3. For comparisons across documents or dates, find the value in EACH relevant document
   and say which document each value came from. If any needed value is missing, set "answerable" to false.
4. Do NOT do arithmetic in your head. Put it in "calculations" as a plain expression using
   only numbers, e.g. "7.1 - 7.8" or "(7.1 - 7.8) / 7.8 * 100". Write the extracted values
   in your answer; the system will compute the result and append it.
5. "used_chunk_ids" must list only the ids of excerpts that directly support your answer.
6. Do not give medical advice or diagnoses beyond what the documents state.
7. Keep the answer short and include units.

Reply with ONLY a JSON object, no markdown, in exactly this form:
{
  "answerable": true or false,
  "answer": "string",
  "used_chunk_ids": [1, 2],
  "calculations": [{"description": "change in HbA1c", "expression": "7.1 - 7.8"}]
}"""


# ---------- safe calculator (no eval!) ----------
_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}


def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("unsupported expression")


def safe_calculate(expression: str):
    return _eval_node(ast.parse(expression, mode="eval").body)


def run_calculations(calculations) -> list[str]:
    lines = []
    for calc in calculations or []:
        try:
            expr = str(calc["expression"])
            result = round(safe_calculate(expr), 2)
            lines.append(f"{calc.get('description', 'Result')}: {expr} = {result:g}")
        except Exception:
            continue  # skip anything we can't verify
    return lines


# ---------- helpers ----------
def refusal() -> dict:
    return {"answer": REFUSAL_ANSWER, "sources": []}


def build_context(chunks: list[dict]) -> str:
    parts = []
    for i, c in enumerate(chunks, start=1):
        parts.append(
            f"[{i}] document: {c['document']} | page: {c['page']} | section: {c['section']}\n{c['text']}"
        )
    return "\n\n".join(parts)


def parse_llm_json(raw: str) -> dict | None:
    try:
        start, end = raw.index("{"), raw.rindex("}") + 1
        return json.loads(raw[start:end])
    except (ValueError, json.JSONDecodeError):
        return None


# ---------- main pipeline ----------
def answer_question(question: str) -> dict:
    # 1. Retrieve
    chunks = store.search(question)
    if not chunks or chunks[0]["score"] < MIN_SCORE:
        return refusal()

    # 2. Ask the LLM, using only the retrieved context
    user_prompt = f"CONTEXT:\n{build_context(chunks)}\n\nQUESTION: {question}"
    parsed = parse_llm_json(ask_llm(SYSTEM_PROMPT, user_prompt))

    # 3. Validate. Anything unusual -> refuse (never guess)
    if not parsed or parsed.get("answerable") is not True:
        return refusal()
    answer = str(parsed.get("answer", "")).strip()
    if not answer:
        return refusal()

    # 4. Build sources ONLY from real retrieved chunks (LLM can't invent them)
    sources, seen = [], set()
    for chunk_id in parsed.get("used_chunk_ids", []):
        if not isinstance(chunk_id, int) or not (1 <= chunk_id <= len(chunks)):
            continue
        c = chunks[chunk_id - 1]
        key = (c["document"], c["page"], c["section"])
        if key not in seen:
            seen.add(key)
            sources.append({"document": c["document"], "page": c["page"], "section": c["section"]})

    if not sources:  # an answer with no evidence is not allowed
        return refusal()

    # 5. Append verified arithmetic
    calc_lines = run_calculations(parsed.get("calculations"))
    if calc_lines:
        answer += "\n\nCalculation: " + "; ".join(calc_lines)

    return {"answer": answer, "sources": sources}