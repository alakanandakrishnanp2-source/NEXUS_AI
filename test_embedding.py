
from modules.embedding_manager import generate_query_embedding

print("Testing Gemini query embedding...", flush=True)

try:
    embedding = generate_query_embedding(
        "How many annual leave days are allowed?"
    )

    print("SUCCESS")
    print("Embedding dimensions:", len(embedding))

except Exception as error:
    print("FAILED:", repr(error))
