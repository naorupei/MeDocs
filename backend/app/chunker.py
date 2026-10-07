from typing import Dict, List, Optional

from app.models import Chunk

CHUNK_SIZE = 1200      # approximate max characters per chunk
CHUNK_OVERLAP = 150    # characters repeated between neighbouring chunks
DEFAULT_SECTION = "General"

# lowercase heading text -> name shown in the "section" field
SECTION_KEYWORDS = {
    "laboratory results": "Laboratory Results",
    "lab results": "Lab Results",
    "blood test": "Blood Test",
    "complete blood count": "Complete Blood Count",
    "cbc": "CBC",
    "biochemistry": "Biochemistry",
    "medications": "Medications",
    "medical history": "Medical History",
    "patient information": "Patient Information",
    "diagnosis": "Diagnosis",
    "observations": "Observations",
    "impression": "Impression",
    "findings": "Findings",
    "radiology": "Radiology",
    "imaging": "Imaging",
    "results": "Results",
    "recommendations": "Recommendations",
    "clinical history": "Clinical History",
}

# Longer keywords first, so "complete blood count" is checked before "cbc"
_LONG_KEYWORDS = sorted(
    [k for k in SECTION_KEYWORDS if len(k) >= 8], key=len, reverse=True
)


def detect_section(line: str) -> Optional[str]:
    """
    If this line looks like a section heading, return the section name.
    Otherwise return None.
    Examples that match: "Laboratory Results", "MEDICATIONS:", "Diagnosis: Anemia"
    """
    line = line.strip()
    if not line or len(line) > 60:
        return None

    candidate = line.split(":")[0].strip().lower()  # text before a colon
    if candidate in SECTION_KEYWORDS:
        return SECTION_KEYWORDS[candidate]

    # allow things like "Complete Blood Count (CBC) Report"
    for kw in _LONG_KEYWORDS:
        if candidate.startswith(kw):
            return SECTION_KEYWORDS[kw]

    return None


def split_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Cut text into pieces of about `size` characters, breaking at spaces/newlines."""
    text = text.strip()
    if not text:
        return []
    if len(text) <= size:
        return [text]

    pieces: List[str] = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            # try to end the chunk at a space or newline instead of mid-word
            cut = max(text.rfind(" ", start, end), text.rfind("\n", start, end))
            if cut > start + size // 2:
                end = cut
        piece = text[start:end].strip()
        if piece:
            pieces.append(piece)
        if end >= len(text):
            break

        new_start = end - overlap
        if new_start <= start:
            new_start = end
        # don't start the next chunk in the middle of a word
        while new_start < end and not text[new_start - 1].isspace():
            new_start += 1
        start = new_start

    return pieces


def chunk_document(
    document_id: str, document: str, pages: List[Dict]
) -> List[Chunk]:
    """
    Turn pages [{"page": 1, "text": "..."}] into a list of Chunk objects.
    Each chunk comes from exactly ONE page and keeps that page number.
    """
    chunks: List[Chunk] = []
    current_section = DEFAULT_SECTION  # carries over from page to page

    for page in pages:
        page_number = page["page"]
        text = page.get("text") or ""
        if not text.strip():
            continue  # empty page: no chunks

        # 1) split this page into (section, text) segments
        segments = []
        buffer: List[str] = []
        for line in text.split("\n"):
            found = detect_section(line)
            if found:
                if "".join(buffer).strip():
                    segments.append((current_section, "\n".join(buffer)))
                buffer = [line]
                current_section = found
            else:
                buffer.append(line)
        if "".join(buffer).strip():
            segments.append((current_section, "\n".join(buffer)))

        # 2) cut each segment into chunks, always using THIS page number
        for section, segment_text in segments:
            for piece in split_text(segment_text):
                chunks.append(
                    Chunk(
                        text=piece,
                        document_id=document_id,
                        document=document,
                        page=page_number,
                        section=section,
                    )
                )

    return chunks