# MEDOCS

### MULTIMODAL MEDICAL DOCUMENT INTELLIGENCE SYSTEM

> STATUS: DEVELOPMENT MVP  
> MISSION: TURN COMPLEX MEDICAL DOCUMENTS INTO TRACEABLE INFORMATION

---

## [ 01 ] MISSION BRIEF

Medical information is often spread across multiple documents such as laboratory reports, prescriptions, discharge summaries, scanned records, tables, and multi-page PDFs.

**Medocs** provides a single interface for processing medical documents and retrieving information through natural-language questions.
---

## Project Overview

**Medocs** is a multimodal medical document intelligence system designed to help users retrieve useful information from medical documents such as laboratory reports, prescriptions, discharge summaries, and other PDF-based records.

Users can upload one or more documents and ask questions about their contents. Medocs processes the uploaded documents, retrieves relevant information, and presents answers together with supporting document and page references.

The system focuses on making medical document analysis faster, easier to navigate, and traceable back to the original source.

Medocs is designed as an **information retrieval and document intelligence system**, not as a medical diagnosis system.

---

## Problem Statement

Medical information is often distributed across multiple documents and formats. Important information may be located across different pages, reports, tables, scanned pages, or other document elements.

Manually searching through multiple medical documents can be time-consuming, especially when users need to find specific information or compare values between reports.

Medocs addresses this problem by providing a centralized document-based question-answering system that allows users to:

- Upload medical documents
- Ask natural-language questions
- Retrieve relevant information
- Compare information across documents
- Trace answers back to their source documents and pages

---

## Key Features

- Upload medical PDF documents
- Process uploaded documents
- Extract relevant document content
- Ask questions using natural language
- Support multiple documents
- Retrieve information across documents
- Provide document-level source information
- Provide page-level source information
- Compare information between reports
- Evidence-backed answers
- Simple web-based interface
- FastAPI-based backend
- Modular architecture for future improvements

---

## System Architecture

The current Medocs workflow follows a document-to-answer pipeline:

```text
                    MEDICAL DOCUMENTS
                           |
                           v
                +---------------------+
                | Document Processing |
                +---------------------+
                           |
                           v
                +---------------------+
                | Text / Content      |
                | Extraction          |
                +---------------------+
                           |
                           v
                +---------------------+
                | Page-Aware          |
                | Processing          |
                +---------------------+
                           |
                           v
                +---------------------+
                | Information         |
                | Retrieval           |
                +---------------------+
                           |
                    USER QUESTION
                           |
                           v
                +---------------------+
                | Query Processing    |
                +---------------------+
                           |
                           v
                +---------------------+
                | Relevant Evidence   |
                | Retrieval           |
                +---------------------+
                           |
                           v
                +---------------------+
                | Question Answering  |
                +---------------------+
                           |
                           v
                +---------------------+
                | Evidence / Source   |
                | Attribution         |
                +---------------------+
                           |
                           v
                 ANSWER + SOURCES
```
---

## Data Pipeline

The data pipeline demonstrates how input documents are collected, processed, retrieved, and passed through the system.

```text
Medical PDF
     |
     v
Document Upload
     |
     v
PDF / Document Processing
     |
     v
Content Extraction
     |
     v
Text + Page Information
     |
     v
Chunking / Processing
     |
     v
Retrieval / Indexing
     |
     v
User Question
     |
     v
Query Processing
     |
     v
Relevant Content Retrieval
     |
     v
AI Question Answering
     |
     v
Evidence Selection
     |
     v
Answer + Document + Page
```
