import io
import re
from typing import Dict, List

from pypdf import PdfReader


class PDFProcessingError(Exception):
    """Raised when a PDF cannot be read. The message is safe to show to API users."""


def _clean_text(text: str) -> str:
    """Tidy up extracted text but KEEP line breaks (we need them to find headings)."""
    text = text.replace("\x00", "").replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)  # at most one blank line in a row
    return text.strip()


def extract_pages(pdf_bytes: bytes) -> List[Dict]:
    """
    Read a PDF and return one item per page:
        [{"page": 1, "text": "..."}, {"page": 2, "text": "..."}]
    Page numbers are 1-based. A page with no text gets "".
    """
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
    except Exception as e:
        raise PDFProcessingError(
            "Could not read this PDF. The file may be corrupted or not a real PDF."
        ) from e

    if reader.is_encrypted:
        try:
            if not reader.decrypt(""):
                raise PDFProcessingError("This PDF is password-protected.")
        except PDFProcessingError:
            raise
        except Exception as e:
            raise PDFProcessingError("This PDF is encrypted and cannot be read.") from e

    try:
        total = len(reader.pages)
    except Exception as e:
        raise PDFProcessingError("Could not read the pages of this PDF.") from e

    if total == 0:
        raise PDFProcessingError("This PDF has no pages.")

    pages: List[Dict] = []
    for index in range(total):
        try:
            raw = reader.pages[index].extract_text() or ""
        except Exception:
            raw = ""  # one bad page must not break the whole document
        pages.append({"page": index + 1, "text": _clean_text(raw)})

    return pages