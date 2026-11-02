from modules.document_processor import extract_text
from modules.text_chunker import create_chunks
from modules.vector_store import store_chunks

file_path = "data/documents/hr_policy.txt"

print("Reading HR policy document...")

text = extract_text(file_path)

print("Creating document chunks...")

chunks = create_chunks(
    text,
    file_path,
    access_level="standard"
)

print("Indexing HR policy into ChromaDB...")

stored = store_chunks(chunks)

print(f"Successfully stored: {stored} chunks")
print("Access level: standard")