from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL


# ==========================================
# GEMINI CLIENT CONFIGURATION
# ==========================================

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(
        timeout=120000
    )
)


# ==========================================
# TEST GEMINI ANSWER GENERATION
# ==========================================

def test_gemini():

    print(
        "Testing Gemini with a minimal request...",
        flush=True
    )

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents="Reply with only: Gemini is working.",
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=100
            )
        )

        if response.text:

            print("\nSUCCESS: Gemini is working!")
            print("\nGemini Response:")
            print(response.text)

        else:

            print("\nFAILED: Gemini returned an empty response.")

    except Exception as error:

        print("\nFAILED: Gemini request unsuccessful.")
        print("Error Type:", type(error).__name__)
        print("Error Details:", str(error))


# ==========================================
# RUN TEST
# ==========================================

if __name__ == "__main__":
    test_gemini()