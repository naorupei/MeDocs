import uuid
from pathlib import Path
from typing import List

from app.models import DocumentMetadata

# backend/app/storage.py -> backend/ -> backend/data/
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"
METADATA_DIR = DATA_DIR / "metadata"


class StorageError(Exception):
    """Raised when a file cannot be saved or read. Message is safe to show to users."""


def ensure_dirs() -> None:
    """Create the data folders if they do not exist yet."""
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)


def new_document_id() -> str:
    """Random unique ID, e.g. '3f2b8c1e9a4d4b7c8e1f5a6b7c8d9e0f'."""
    return uuid.uuid4().hex


def save_pdf(document_id: str, pdf_bytes: bytes) -> Path:
    """Save the uploaded PDF as data/documents/<document_id>.pdf"""
    try:
        ensure_dirs()
        path = DOCUMENTS_DIR / f"{document_id}.pdf"
        path.write_bytes(pdf_bytes)
        return path
    except OSError as e:
        raise StorageError("Could not save the PDF file on the server.") from e


def delete_pdf(document_id: str) -> None:
    """Remove a saved PDF (used to clean up if processing fails)."""
    try:
        (DOCUMENTS_DIR / f"{document_id}.pdf").unlink(missing_ok=True)
    except OSError:
        pass


def save_metadata(metadata: DocumentMetadata) -> Path:
    """Save document info as data/metadata/<document_id>.json"""
    try:
        ensure_dirs()
        path = METADATA_DIR / f"{metadata.document_id}.json"
        path.write_text(metadata.model_dump_json(indent=2), encoding="utf-8")
        return path
    except OSError as e:
        raise StorageError("Could not save the document metadata.") from e


def list_metadata() -> List[DocumentMetadata]:
    """Read every metadata file and return them, oldest upload first."""
    ensure_dirs()
    files = sorted(METADATA_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime)
    documents: List[DocumentMetadata] = []
    for file in files:
        try:
            documents.append(
                DocumentMetadata.model_validate_json(file.read_text(encoding="utf-8"))
            )
        except Exception:
            continue  # skip any damaged file instead of crashing
    return documents