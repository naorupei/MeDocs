"""Loads fake chunks so you can test /chat without Member 2.
Run the server first, then: uv run python scripts/load_sample.py"""
import json
import urllib.request

chunks = [
    {"text": "Patient: A. Sharma. Visit date: 15 January 2026. Diagnosis: Type 2 diabetes mellitus.",
     "document_id": "jan", "document": "January.pdf", "page": 1, "section": "Patient Summary"},
    {"text": "Laboratory Results: HbA1c 7.8 %. Fasting glucose 156 mg/dL. Creatinine 0.9 mg/dL.",
     "document_id": "jan", "document": "January.pdf", "page": 2, "section": "Laboratory Results"},
    {"text": "Medications: Metformin 500 mg twice daily.",
     "document_id": "jan", "document": "January.pdf", "page": 3, "section": "Medications"},
    {"text": "Patient: A. Sharma. Visit date: 18 June 2026. Follow-up for Type 2 diabetes mellitus.",
     "document_id": "jun", "document": "June.pdf", "page": 1, "section": "Patient Summary"},
    {"text": "Laboratory Results: HbA1c 7.1 %. Fasting glucose 128 mg/dL. Creatinine 0.9 mg/dL.",
     "document_id": "jun", "document": "June.pdf", "page": 3, "section": "Laboratory Results"},
    {"text": "Medications: Metformin 1000 mg twice daily. Added Empagliflozin 10 mg once daily.",
     "document_id": "jun", "document": "June.pdf", "page": 4, "section": "Medications"},
]

req = urllib.request.Request(
    "http://localhost:8000/ingest",
    data=json.dumps({"chunks": chunks}).encode(),
    headers={"Content-Type": "application/json"},
)
print(urllib.request.urlopen(req).read().decode())