
from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_EMBEDDING_MODEL


client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(timeout=15000)
)


def generate_embedding(text, task_type="RETRIEVAL_DOCUMENT"):

    if not text or not text.strip():
        raise ValueError("Cannot generate embedding for empty text.")

    print("Generating embedding...", flush=True)

    response = client.models.embed_content(
        model=GEMINI_EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type=task_type
        )
    )

    print("Embedding generated successfully.", flush=True)

    return response.embeddings[0].values


def generate_query_embedding(text):

    return generate_embedding(
        text,
        task_type="RETRIEVAL_QUERY"
    )
