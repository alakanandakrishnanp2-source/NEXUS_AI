import chromadb
from collections import defaultdict

client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = client.get_collection(
    name="nexus_documents"
)

results = collection.get(include=["metadatas"])

documents = defaultdict(lambda: {
    "chunks": 0,
    "category": set(),
    "access_level": set()
})

for metadata in results["metadatas"]:
    source = metadata.get("source", "Unknown")

    documents[source]["chunks"] += 1
    documents[source]["category"].add(
        metadata.get("category", "Unknown")
    )
    documents[source]["access_level"].add(
        metadata.get("access_level", "Unknown")
    )

print("\n===== NEXUS AI DOCUMENT INDEX =====")
print("Total indexed chunks:", collection.count())
print("Unique indexed documents:", len(documents))

for source, details in documents.items():
    print("\nDocument:", source)
    print("Chunks:", details["chunks"])
    print("Category:", details["category"])
    print("Access Level:", details["access_level"])

print("\n===================================")