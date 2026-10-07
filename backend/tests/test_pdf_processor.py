import sys
from pathlib import Path

import pytest

# Make "app" and "make_sample_pdf" importable when running pytest
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from make_sample_pdf import BLOOD_REPORT, SECOND_REPORT, make_pdf  # noqa: E402

from app.chunker import chunk_document, detect_section, split_text  # noqa: E402
from app.pdf_processor import PDFProcessingError, extract_pages  # noqa: E402


def test_valid_pdf_page_numbers_are_one_based():
    pages = extract_pages(make_pdf(BLOOD_REPORT))
    assert [p["page"] for p in pages] == [1, 2, 3]


def test_text_is_on_the_right_page():
    pages = extract_pages(make_pdf(BLOOD_REPORT))
    assert "Hemoglobin" in pages[1]["text"]       # page 2
    assert "Hemoglobin" not in pages[0]["text"]   # not page 1


def test_empty_page_returns_empty_string():
    pages = extract_pages(make_pdf(SECOND_REPORT))
    assert len(pages) == 3
    assert pages[1]["page"] == 2
    assert pages[1]["text"] == ""


def test_invalid_pdf_raises_clear_error():
    with pytest.raises(PDFProcessingError):
        extract_pages(b"this is not a pdf")


def test_chunks_keep_page_numbers_and_fields():
    pages = extract_pages(make_pdf(BLOOD_REPORT))
    chunks = chunk_document("doc1", "blood_report.pdf", pages)
    assert {c.page for c in chunks} == {1, 2, 3}
    for c in chunks:
        assert c.document_id == "doc1"
        assert c.document == "blood_report.pdf"
        assert c.section
        assert c.text.strip()
    # Hemoglobin text must only appear in page 2 chunks
    assert all(c.page == 2 for c in chunks if "Hemoglobin" in c.text)


def test_sections_are_detected():
    pages = extract_pages(make_pdf(BLOOD_REPORT))
    chunks = chunk_document("doc1", "blood_report.pdf", pages)
    sections = {(c.page, c.section) for c in chunks}
    assert (2, "Laboratory Results") in sections
    assert (3, "Recommendations") in sections


def test_chunks_never_mix_pages():
    pages = [
        {"page": 1, "text": "ALPHA text on page one"},
        {"page": 2, "text": "BETA text on page two"},
    ]
    chunks = chunk_document("d", "x.pdf", pages)
    for c in chunks:
        assert not ("ALPHA" in c.text and "BETA" in c.text)
    assert [c.page for c in chunks] == [1, 2]


def test_section_falls_back_to_general():
    chunks = chunk_document("d", "x.pdf", [{"page": 1, "text": "Just some random notes."}])
    assert len(chunks) == 1
    assert chunks[0].section == "General"


def test_detect_section_basic():
    assert detect_section("Laboratory Results") == "Laboratory Results"
    assert detect_section("MEDICATIONS:") == "Medications"
    assert detect_section("The patient feels fine today.") is None


def test_long_page_is_split_but_keeps_page_number():
    text = " ".join(f"word{i}" for i in range(1000))
    chunks = chunk_document("d", "x.pdf", [{"page": 5, "text": text}])
    assert len(chunks) > 1
    assert all(c.page == 5 for c in chunks)
    assert all(len(c.text) <= 1300 for c in chunks)


def test_split_text_empty():
    assert split_text("   ") == []