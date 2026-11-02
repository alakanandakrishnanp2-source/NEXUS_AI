
import pymupdf
from docx import Document
from pathlib import Path


def extract_pdf_pages(file_path):
    """Extract PDF text page by page."""

    pages = []

    pdf = pymupdf.open(file_path)

    for page_number, page in enumerate(pdf, start=1):
        pages.append({
            "text": page.get_text(),
            "page_number": page_number
        })

    pdf.close()
    return pages


def extract_pdf(file_path):
    """Extract complete PDF text."""

    pages = extract_pdf_pages(file_path)

    return "\n".join(
        f"[Page {page['page_number']}]\n{page['text']}"
        for page in pages
    )


def extract_docx(file_path):
    """Extract Word document text."""

    document = Document(file_path)

    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )


def extract_txt(file_path):
    """Extract TXT document text."""

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_text(file_path):
    """Identify file type and extract text."""

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    elif extension == ".docx":
        return extract_docx(file_path)

    elif extension == ".txt":
        return extract_txt(file_path)

    else:
        raise ValueError(
            "Unsupported file format. Use PDF, DOCX, or TXT."
        )
