# MEDOCS

### MULTIMODAL MEDICAL DOCUMENT INTELLIGENCE SYSTEM

> `STATUS: DEVELOPMENT MVP`
>
> `MISSION: TURN COMPLEX MEDICAL DOCUMENTS INTO TRACEABLE INFORMATION`

---

<div align="center">

```text
███╗   ███╗███████╗██████╗  ██████╗  ██████╗███████╗
████╗ ████║██╔════╝██╔══██╗██╔═══██╗██╔════╝██╔════╝
██╔████╔██║█████╗  ██║  ██║██║   ██║██║     ███████╗
██║╚██╔╝██║██╔══╝  ██║  ██║██║   ██║██║     ╚════██║
██║ ╚═╝ ██║███████╗██████╔╝╚██████╔╝╚██████╗███████║
╚═╝     ╚═╝╚══════╝╚═════╝  ╚═════╝  ╚═════╝╚══════╝
```
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

The system is designed to preserve document and page information throughout the processing pipeline so that retrieved information can be traced back to its original location.

---

## Core Model / Reasoning

The core functionality of Medocs is based on document retrieval followed by question answering.

When a user submits a question, the system identifies relevant information from the uploaded documents and uses that information to construct the response.

The general reasoning flow is:

```text
User Question
      |
      v
Question Processing
      |
      v
Relevant Document Content
      |
      v
Evidence Retrieval
      |
      v
Answer Generation
      |
      v
Source Attribution
      |
      v
Final Response
```

The current MVP uses the AI and retrieval components implemented during development.

The retrieval architecture is modular and can be extended with additional ranking, query analysis, and reasoning mechanisms in future versions.

---

## Evidence & Source Attribution

A major objective of Medocs is to make answers traceable.

Instead of returning only a generated answer, the system is designed to associate the answer with the document content used to produce it.

Example:

```text
Answer:
HbA1c decreased from 7.8% to 7.1%.

Evidence:
Blood_Report_January.pdf
Page 2

Blood_Report_June.pdf
Page 3
```

This allows users and evaluators to verify where the information came from.

The evidence structure can include:

```text
Document Name
Page Number
Relevant Content
Answer
```

This is particularly important for medical documents where users should be able to trace information back to the original source.

---

## Sample Input & Output

### Sample Input

Documents:

```text
Blood_Report_January.pdf
Blood_Report_June.pdf
```

Question:

```text
How did HbA1c change between January and June?
```

### Sample Output

```text
HbA1c decreased from 7.8% in January to 7.1% in June.
```

Evidence:

```text
Blood_Report_January.pdf — Page 2
Blood_Report_June.pdf — Page 3
```

The exact values and pages depend on the sample documents used during the demonstration.

---

## Technologies Used

### Backend

- Python
- FastAPI

### Frontend

- HTML
- CSS
- JavaScript

### Development

- Git
- GitHub
- uv

### AI / Retrieval

The current MVP uses the AI and retrieval components implemented during development.

The architecture is designed to support future improvements to retrieval, ranking, reasoning, OCR, and multimodal document understanding.

---

## Project Structure

```text
Medocs/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   ├── core/
│   │   └── main.py
│   │
│   └── tests/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── data/
│   └── sample/
│
├── docs/
│
├── .env.example
├── .gitignore
├── README.md
└── pyproject.toml
```

> Update the structure above if the final repository structure differs.

---

## Team Contributions

### Member 1 — AI & Backend

Responsible for the core backend and intelligence layer.

Responsibilities:

- FastAPI backend
- AI integration
- Retrieval integration
- Question-answering pipeline
- Evidence response structure
- Backend integration
- API development

### Member 2 — Frontend

Responsible for the user-facing interface.

Responsibilities:

- Web interface
- Document upload interface
- Document list
- Question interface
- Answer display
- Evidence display
- Frontend-backend integration

### Member 3 — Document, Evidence & Testing

Responsible for document handling, evidence support, and validation.

Responsibilities:

- Document processing
- Page handling
- Evidence presentation
- Sample documents
- Test cases
- System testing
- Validation

---

## Branch Structure

The project was developed collaboratively using Git and GitHub.

### `main`

The stable base branch.

No direct development work is intended to be performed directly on `main`.

### `dev`

The **complete merged project is currently maintained in the `dev` branch**.

The `dev` branch contains the integrated work from all three team members and represents the current development version of Medocs.

It is also being used as the base for future development and additional features.

### Individual Feature Branches

Individual members worked on separate branches for their assigned components.

```text
feature/ai-backend
feature/frontend
feature/document-evidence
```

Each member develops their assigned functionality independently before integrating the completed work into `dev`.

---

## Installation

### Requirements

Make sure the following are installed:

- Python
- Git
- uv

Clone the repository:

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd Medocs
```

Switch to the development branch:

```bash
git checkout dev
```

---

## Install Dependencies

The project uses `uv` for dependency management.

Run:

```bash
uv sync
```

This installs the dependencies defined by the project configuration.

---

## Configuration

Create a local environment file using the provided example:

```bash
cp .env.example .env
```

Add the required configuration values to `.env`.

Do not commit private API keys or credentials to GitHub.

---

## Running the Backend

Start the FastAPI application using the project's configured entry point.

For example:

```bash
uv run uvicorn app.main:app --reload
```

If the final project structure uses a different application path, use the corresponding entry point defined in the repository.

---

## Running the Frontend

Open the frontend using the project's local development setup.

The frontend communicates with the FastAPI backend to:

```text
Upload Documents
       |
       v
Backend Processing
       |
       v
Ask Questions
       |
       v
Retrieve Answers
       |
       v
Display Evidence
```

---

## Reproducing the Demonstration

The demonstrated results can be reproduced using the sample documents included with the project.

### Step 1

Clone the repository.

### Step 2

Switch to the `dev` branch.

```bash
git checkout dev
```

### Step 3

Install dependencies.

```bash
uv sync
```

### Step 4

Configure the required environment variables.

### Step 5

Start the backend.

### Step 6

Open the frontend.

### Step 7

Upload the sample medical documents from:

```text
data/sample/
```

### Step 8

Ask the demonstrated question.

Example:

```text
How did HbA1c change between January and June?
```

### Step 9

Verify that the system returns:

```text
Answer
+
Document Source
+
Page Number
+
Supporting Evidence
```

---

## Example Demonstration Flow

The complete live demonstration can follow this sequence:

```text
1. Open Medocs
        |
        v
2. Upload medical PDFs
        |
        v
3. Documents are processed
        |
        v
4. Ask a question
        |
        v
5. System retrieves relevant information
        |
        v
6. AI generates the response
        |
        v
7. Evidence is attached
        |
        v
8. Answer is displayed with source/page
```

This demonstrates the complete pipeline from input to output.

---

## Minimum Viable Product

The current MVP focuses on the essential functionality required for the problem:

- Medical PDF upload
- Document processing
- Information retrieval
- Natural-language questions
- Question answering
- Multi-document support
- Document/page-level evidence
- Basic cross-document comparison
- Functional web interface
- FastAPI backend

The MVP prioritizes a working end-to-end system over advanced features that require significantly more development time.

---

## Future Scope

The architecture can be extended with:

- Custom RAG implementation
- Page-aware indexing
- Improved query analysis
- Keyword and entity matching
- Custom relevance scoring
- Evidence ranking
- Advanced numerical reasoning
- Improved OCR
- Table understanding
- Chart understanding
- Visual document analysis
- Evidence highlighting
- Contradiction detection
- Medical document timelines
- Advanced cross-document reasoning
- Better handling of scanned documents
- Improved multimodal retrieval

These features are considered extensions beyond the current MVP unless explicitly implemented in the final submitted version.

---

## Current Development Status

```text
STATUS: DEVELOPMENT MVP

CORE SYSTEM:
[ ACTIVE ]

DOCUMENT PROCESSING:
[ ACTIVE ]

RETRIEVAL:
[ ACTIVE ]

QUESTION ANSWERING:
[ ACTIVE ]

EVIDENCE / SOURCE ATTRIBUTION:
[ ACTIVE ]

ADVANCED CUSTOM RAG:
[ FUTURE SCOPE ]
```

The integrated project is currently maintained in the `dev` branch.

---

## Limitations

The current MVP may be affected by:

- Poor-quality PDFs
- Incorrectly formatted documents
- Low-quality scanned pages
- OCR limitations
- Complex tables
- Complex charts
- Unusual document layouts
- Missing or incomplete document information
- Ambiguous questions

The accuracy of the final response depends on the quality and content of the uploaded documents and the implemented retrieval and AI components.

---

## Medical Disclaimer

Medocs is a medical document intelligence and information retrieval system.

It is **not a diagnostic system**.

Medocs does not provide:

- Medical diagnoses
- Treatment recommendations
- Medication advice
- Professional medical advice

Information retrieved by Medocs should not be treated as a substitute for consultation with a qualified healthcare professional.

---

## Development

Medocs was developed as a collaborative hackathon project focused on building a working multimodal medical document intelligence MVP within a limited development timeframe.

The project emphasizes:

```text
DOCUMENTS
    +
RETRIEVAL
    +
QUESTION ANSWERING
    +
EVIDENCE
    =
TRACEABLE MEDICAL INFORMATION
```

The architecture is modular so that future improvements can be added without requiring a complete redesign of the system.

---

## Repository

The complete source code, documentation, configuration, sample data, and development history are maintained in the project's public Git repository.

The `dev` branch represents the current integrated development version, while `main` represents the stable base branch.

---

## Final Demo

The recommended demonstration should show the complete workflow:

```text
UPLOAD
  ↓
PROCESS
  ↓
ASK
  ↓
RETRIEVE
  ↓
REASON
  ↓
ANSWER
  ↓
VERIFY SOURCE
```

**Medocs — turning complex medical documents into traceable information.**
