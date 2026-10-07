# Medocs - Document Processing Backend

This backend takes uploaded PDFs, extracts the text **page by page**, cuts it into
**page-aware chunks**, and stores everything locally. Member 1's RAG system reads these chunks.

## What it does
- Upload PDFs (multiple supported), validate them, store them
- Extract text per page (page numbers start at 1)
- Split into chunks (~1200 chars, ~150 overlap) that never mix pages
- Detect simple section headings (e.g. "Laboratory Results"), otherwise `"General"`
- Save document metadata and list all documents

## What it does NOT do
No RAG, no LLM, no embeddings, no vector DB, no OCR (scanned PDFs return no text), no frontend, no authentication.

## Install and run (Windows PowerShell)
```powershell
cd backend
uv sync
uv run uvicorn app.main:app --reload
```
- API: http://127.0.0.1:8000
- Swagger (try the API in the browser): http://127.0.0.1:8000/docs

## Run tests
```powershell
uv run python tests/make_sample_pdf.py   # creates fake PDFs (synthetic data)
uv run pytest -v
```

## Endpoints
| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Service info |
| GET | `/health` | Health check, returns `{"status": "ok"}` |
| POST | `/documents/upload` | Upload one PDF (form field name: `file`) |
| GET | `/documents` | List metadata of all uploaded documents |

### Upload example
```powershell
curl.exe -X POST -F "file=@tests/sample_blood_report.pdf" http://127.0.0.1:8000/documents/upload
```
To upload several PDFs, call the endpoint once per file.

### Upload response
```json
{
  "message": "Document uploaded and processed successfully.",
  "metadata": {
    "document_id": "3f2b8c1e9a4d4b7c8e1f5a6b7c8d9e0f",
    "document": "blood_report.pdf",
    "total_pages": 3,
    "total_chunks": 4,
    "file_size": 12345
  },
  "chunks": [
    {
      "text": "Laboratory Results\nHemoglobin 10.2 g/dL (ref 12.0-15.5) LOW ...",
      "document_id": "3f2b8c1e9a4d4b7c8e1f5a6b7c8d9e0f",
      "document": "blood_report.pdf",
      "page": 2,
      "section": "Laboratory Results"
    }
  ]
}
```

### GET /documents response
```json
{
  "documents": [
    {"document_id": "...", "document": "blood_report.pdf", "total_pages": 3, "total_chunks": 4, "file_size": 12345}
  ],
  "count": 1
}
```

## Chunk structure (the contract for Member 1)
Every chunk has exactly these 5 fields:

| Field | Meaning |
|---|---|
| `text` | The chunk text |
| `document_id` | Unique ID of the uploaded PDF |
| `document` | Original filename |
| `page` | **1-based** page number (PDF page 1 -> `1`) |
| `section` | Detected heading, or `"General"` (never missing) |

Rules:
- A chunk never contains text from two pages, so `page` is always exact. Use it for citations.
- A section carries over to following pages until a new heading appears.
- Blank pages produce no chunks.
- If `chunks` is empty, the PDF probably has no text layer (scanned image).

## How Member 1 should consume the chunks
1. Call `POST /documents/upload` and read the `chunks` list from the response, or
2. Call `GET /documents` for the list of documents.
3. Index each chunk's `text` and keep `document`, `page` and `section` as metadata
   so answers can cite "blood_report.pdf, page 2".

## Storage
```
data/
  documents/<document_id>.pdf      uploaded PDFs (random ID, not the original filename)
  metadata/<document_id>.json      one metadata file per document
```
These folders are git-ignored. Never commit real medical documents. Test only with synthetic PDFs.

## Project layout
```
app/main.py           FastAPI endpoints
app/models.py         Pydantic models (Chunk, DocumentMetadata, ...)
app/pdf_processor.py  Page-by-page text extraction (pypdf)
app/chunker.py        Section detection and chunking
app/storage.py        Saving PDFs and metadata to disk
tests/                Tests and a fake-PDF generator
```