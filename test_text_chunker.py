
from modules.document_processor import extract_text
from modules.text_chunker import create_chunks

file_path = input("Enter document path: ")

try:
    text = extract_text(file_path)

    chunks = create_chunks(
        text,
        source_file=file_path,
        chunk_size=100,
        chunk_overlap=20
    )

    print("\nCHUNKING AND METADATA SUCCESSFUL")
    print("=" * 50)

    for chunk in chunks:

        print("\nCHUNK:", chunk["metadata"]["chunk_id"])
        print("TEXT:", chunk["text"])
        print("METADATA:", chunk["metadata"])

except Exception as error:
    print("Error:", error)
