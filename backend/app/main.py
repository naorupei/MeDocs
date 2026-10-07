from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.chunker import chunk_document
from app.models import DocumentListResponse, DocumentMetadata, UploadResponse
from app.pdf_processor import PDFProcessingError, extract_pages

MAX_UPLOAD_MB = 25
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024

app = FastAPI(
    title="MediLens Document Processing API",
    description="Upload PDFs, extract text page by page, and get page-aware chunks.",
    version="0.1.0",
)

# Lets the frontend (running on another port) call this API during the hackathon.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "service": "MediLens Document Processing API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/documents/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    # 1) Check the filename
    if not file.filename or not file.filename.strip():
        raise HTTPException(status_code=400, detail="No filename was provided.")
    original_name = Path(file.filename).name  # drop any folder path

    if not original_name.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400, detail="Only PDF files are allowed (file must end in .pdf)."
        )

    # 2) Read and check the file contents
    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")
    if len(pdf_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413, detail=f"File is too large. Maximum is {MAX_UPLOAD_MB} MB."
        )
    if not pdf_bytes.lstrip()[:5] == b"%PDF-":
        raise HTTPException(
            status_code=400, detail="This file is not a valid PDF (wrong file signature)."
        )

    # 3) Extract text page by page BEFORE saving anything
    try:
        pages = extract_pages(pdf_bytes)
    except PDFProcessingError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=500, detail="Something went wrong while reading the PDF."
        )

    # 4) Make an ID, chunk the pages
    document_id = storage.new_document_id()
    try:
        chunks = chunk_document(document_id, original_name, pages)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Something went wrong while processing the PDF text."
        )

    metadata = DocumentMetadata(
        document_id=document_id,
        document=original_name,
        total_pages=len(pages),
        total_chunks=len(chunks),
        file_size=len(pdf_bytes),
    )

    # 5) Save the PDF and its metadata
    try:
        storage.save_pdf(document_id, pdf_bytes)
        storage.save_metadata(metadata)
    except storage.StorageError as e:
        storage.delete_pdf(document_id)  # don't leave a half-saved document
        raise HTTPException(status_code=500, detail=str(e))

    if chunks:
        message = "Document uploaded and processed successfully."
    else:
        message = (
            "Document uploaded, but no extractable text was found. "
            "It may be a scanned PDF (OCR is not supported yet)."
        )

    return UploadResponse(message=message, metadata=metadata, chunks=chunks)


@app.get("/documents", response_model=DocumentListResponse)
def list_documents():
    documents = storage.list_metadata()
    return DocumentListResponse(documents=documents, count=len(documents))