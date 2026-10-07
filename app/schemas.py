from pydantic import BaseModel


class Chunk(BaseModel):
    """Format provided by Member 2."""
    text: str
    document_id: str
    document: str
    page: int
    section: str = ""


class IngestRequest(BaseModel):
    chunks: list[Chunk]


class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    document: str
    page: int
    section: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]