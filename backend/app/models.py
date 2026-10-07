from typing import List

from pydantic import BaseModel


class Chunk(BaseModel):
    """One piece of text from one PDF page (this is what Member 1's RAG uses)."""
    text: str
    document_id: str
    document: str      # original filename, e.g. "blood_report.pdf"
    page: int          # 1-based page number
    section: str       # e.g. "Laboratory Results" or "General"


class DocumentMetadata(BaseModel):
    """Summary information about one uploaded PDF."""
    document_id: str
    document: str
    total_pages: int
    total_chunks: int
    file_size: int     # in bytes


class UploadResponse(BaseModel):
    message: str
    metadata: DocumentMetadata
    chunks: List[Chunk]


class DocumentListResponse(BaseModel):
    documents: List[DocumentMetadata]
    count: int