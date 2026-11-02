
from modules.document_processor import extract_text
from modules.text_chunker import create_chunks
from modules.vector_store import store_chunks

file_path = "data/documents/finance_report.txt"

print("Reading financial report...")

text = extract_text(file_path)

chunks = create_chunks(
    text=text,
    source_file=file_path,
    access_level="standard"
)

print("Indexing financial report...")

stored = store_chunks(chunks)

print("Successfully stored:", stored, "chunks")
print("Access level: standard")
