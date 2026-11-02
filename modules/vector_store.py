
import chromadb

from modules.embedding_manager import (
    generate_embedding,
    generate_query_embedding
)


# 1. Create persistent ChromaDB storage
client = chromadb.PersistentClient(
    path="data/chroma_db"
)


# 2. Create or load collection
collection = client.get_or_create_collection(
    name="nexus_documents",
    metadata={"hnsw:space": "cosine"}
)


# 3. Store document chunks
def store_chunks(chunks):
    """Store document chunks and embeddings in ChromaDB."""

    if not chunks:
        return 0

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for chunk in chunks:

        text = chunk["text"]
        metadata = chunk["metadata"]

        if not text or not text.strip():
            continue

        ids.append(
            f"{metadata['source']}_{metadata['chunk_id']}"
        )

        documents.append(text)

        clean_metadata = {
            key: value
            for key, value in metadata.items()
            if value is not None
        }

        metadatas.append(clean_metadata)

        embeddings.append(generate_embedding(text))

    if not ids:
        return 0

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    return len(ids)


# 4. Search documents with role and category filters
def search_documents(
    question,
    top_k=3,
    user_role="standard",
    category=None
):
    """
    Search relevant documents while enforcing access permissions.

    Admin:
        Can access all document categories.

    Standard:
        Can access only public and standard documents.

    Category:
        Optional filter, such as HR or Finance.
    """

    if not question or not question.strip():
        raise ValueError("Search question cannot be empty.")

    if user_role not in ("admin", "standard"):
        raise ValueError("Invalid user role.")

    if category is not None:
        category = category.strip().lower()

        if category not in ("hr", "finance", "general"):
            raise ValueError("Invalid document category.")

    if top_k < 1:
        raise ValueError("top_k must be greater than zero.")

    total_chunks = collection.count()

    if total_chunks == 0:
        return []

    query_embedding = generate_query_embedding(question)

    # Build mandatory access filter first.
    filters = []

    if user_role == "standard":
        filters.append({
            "access_level": {
                "$in": ["public", "standard"]
            }
        })

    # Add category filter when requested.
    if category:
        filters.append({
            "category": {
                "$eq": category
            }
        })

    where_filter = None

    if len(filters) == 1:
        where_filter = filters[0]

    elif len(filters) > 1:
        where_filter = {
            "$and": filters
        }

    query_arguments = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
        "include": [
            "documents",
            "metadatas",
            "distances"
        ]
    }

    if where_filter:
        query_arguments["where"] = where_filter

    results = collection.query(**query_arguments)

    search_results = []

    for index in range(len(results["ids"][0])):

        search_results.append({
            "text": results["documents"][0][index],
            "metadata": results["metadatas"][0][index],
            "distance": results["distances"][0][index]
        })

    return search_results


# 5. Get total stored chunks
def get_document_count():
    """Return the total number of stored chunks."""
    return collection.count()
