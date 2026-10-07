from pathlib import Path


def make_pdf(pages_lines):
    """
    Build a simple text PDF with no extra libraries.
    pages_lines = [["line 1", "line 2"], ["page 2 line"], []]  (an empty list = blank page)
    """
    n = len(pages_lines)
    kids = " ".join(f"{4 + 2 * i} 0 R" for i in range(n))
    objs = {
        1: b"<< /Type /Catalog /Pages 2 0 R >>",
        2: f"<< /Type /Pages /Kids [{kids}] /Count {n} >>".encode(),
        3: b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    }
    for i, lines in enumerate(pages_lines):
        page_id = 4 + 2 * i
        content_id = page_id + 1
        objs[page_id] = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 3 0 R >> >> /Contents {content_id} 0 R >>"
        ).encode()
        parts = ["BT", "/F1 12 Tf", "16 TL", "72 720 Td"]
        for line in lines:
            safe = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            parts.append(f"({safe}) Tj T*")
        parts.append("ET")
        stream = "\n".join(parts).encode("latin-1")
        objs[content_id] = (
            b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n"
            + stream + b"\nendstream"
        )

    out = bytearray(b"%PDF-1.4\n")
    offsets = {}
    for num in sorted(objs):
        offsets[num] = len(out)
        out += f"{num} 0 obj\n".encode() + objs[num] + b"\nendobj\n"
    xref_pos = len(out)
    size = max(objs) + 1
    out += f"xref\n0 {size}\n".encode()
    out += b"0000000000 65535 f \n"
    for num in range(1, size):
        out += f"{offsets[num]:010d} 00000 n \n".encode()
    out += (
        f"trailer\n<< /Size {size} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n"
    ).encode()
    return bytes(out)


BLOOD_REPORT = [
    [
        "Patient Information",
        "Name: Jane Doe (SYNTHETIC TEST DATA)",
        "Age: 45   Sex: F",
        "Medical History",
        "Mild iron deficiency noted in 2023.",
    ],
    [
        "Laboratory Results",
        "Hemoglobin 10.2 g/dL (ref 12.0-15.5) LOW",
        "WBC 7.1 x10^9/L (ref 4.0-11.0) NORMAL",
        "Glucose fasting 132 mg/dL (ref 70-99) HIGH",
    ],
    [
        "Recommendations",
        "Start iron supplementation.",
        "Repeat blood count in 6 weeks.",
    ],
]

SECOND_REPORT = [
    [
        "Radiology",
        "Chest X-ray (SYNTHETIC TEST DATA)",
        "Findings",
        "No acute abnormality seen.",
    ],
    [],  # intentionally blank page
    [
        "Impression",
        "Normal chest radiograph.",
    ],
]


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    (folder / "sample_blood_report.pdf").write_bytes(make_pdf(BLOOD_REPORT))
    (folder / "sample_second_report.pdf").write_bytes(make_pdf(SECOND_REPORT))
    print("Created: tests/sample_blood_report.pdf and tests/sample_second_report.pdf")