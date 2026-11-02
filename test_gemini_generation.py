
from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(timeout=30000)
)

print("Testing Gemini with a minimal request...", flush=True)

try:
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents="Reply with only: Gemini is working."
    )

    print("SUCCESS")
    print(response.text)

except Exception as error:
    print("FAILED:", repr(error))
