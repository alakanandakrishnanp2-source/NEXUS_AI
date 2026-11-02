
from modules.document_processor import extract_text
from modules.text_chunker import create_chunks
from modules.vector_store import store_chunks

file_path = "data/documents/confidential_salary.txt"

print("Reading confidential document...")

text = extract_text(file_path)

chunks = create_chunks(
    text=text,
    source_file=file_path,
    access_level="admin"
)

stored = store_chunks(chunks)

print("Successfully stored:", stored, "chunks")
print("Access level: admin")

