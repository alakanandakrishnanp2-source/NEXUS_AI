
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from modules.document_processor import extract_pdf_pages


VALID_ACCESS_LEVELS = ("public", "standard", "admin")


def get_document_category(file_path):
    """Identify document category from its filename."""

    filename = file_path.name.lower()

    if "hr" in filename or "employee" in filename:
        return "hr"

    elif "finance" in filename:
        return "finance"

    return "general"


def create_chunks(
    text,
    source_file,
    chunk_size=500,
    chunk_overlap=50,
    access_level="standard"
):
    """Split documents into chunks and attach metadata."""

    if not text or not text.strip():
        return []

    if access_level not in VALID_ACCESS_LEVELS:
        raise ValueError("Invalid document access level.")

    file_path = Path(source_file)
    extension = file_path.suffix.lower()

    category = get_document_category(file_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks_with_metadata = []

    def add_chunks(text_chunks, page_number=None):

        for chunk in text_chunks:

            metadata = {
                "source": file_path.name,
                "file_type": extension.replace(".", ""),
                "chunk_id": len(chunks_with_metadata) + 1,
                "access_level": access_level,
                "category": category
            }

            if page_number is not None:
                metadata["page_number"] = page_number

            chunks_with_metadata.append({
                "text": chunk,
                "metadata": metadata
            })

    if extension == ".pdf":

        pages = extract_pdf_pages(source_file)

        for page in pages:
            page_chunks = splitter.split_text(page["text"])
            add_chunks(page_chunks, page["page_number"])

    else:

        text_chunks = splitter.split_text(text)
        add_chunks(text_chunks)

    return chunks_with_metadata
