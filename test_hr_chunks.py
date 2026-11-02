from modules.vector_store import collection

results = collection.get(
    where={
        "category": {
            "$eq": "hr"
        }
    },
    include=["documents", "metadatas"]
)

print("\nFIRST HR CHUNK")
print("=" * 50)

for i, document in enumerate(results["documents"]):
    if results["metadatas"][i]["chunk_id"] == 1:
        print(document)
        print("\nMetadata:", results["metadatas"][i])