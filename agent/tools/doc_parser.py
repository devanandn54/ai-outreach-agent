"""Document parser for PDF and DOCX resumes."""

import fitz  # PyMuPDF
from docx import Document


def extract_text(file_path: str) -> str:
    """Extract text from PDF or DOCX file."""
    if file_path.lower().endswith(".pdf"):
        doc = fitz.open(file_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text
    elif file_path.lower().endswith((".docx", ".doc")):
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    else:
        with open(file_path, "r") as f:
            return f.read()
