
from modules.vector_store import search_documents

print("Starting ChromaDB retrieval test...", flush=True)

try:
    results = search_documents(
        "How many annual leave days are allowed?",
        top_k=5,
        user_role="admin",
        category="hr"
    )

    print("\nRetrieved documents:", len(results))

    for result in results:
        print("\nSource:", result["metadata"].get("source"))
        print("Content:", result["text"][:300])

    print("\nRETRIEVAL TEST COMPLETED")

except Exception as error:
    print("\nRETRIEVAL FAILED:", repr(error))
