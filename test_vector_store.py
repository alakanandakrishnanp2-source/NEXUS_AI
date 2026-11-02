
from modules.document_processor import extract_text
from modules.text_chunker import create_chunks
from modules.vector_store import store_chunks

file_path = "data/documents/sample.docx"

print("Reading document...")

text = extract_text(file_path)

print("Creating standard-access chunks...")

chunks = create_chunks(
    text=text,
    source_file=file_path,
    access_level="standard"
)

print("Storing document with permissions...")

stored = store_chunks(chunks)

print("Successfully stored:", stored, "chunks")
print("Access level: standard")
