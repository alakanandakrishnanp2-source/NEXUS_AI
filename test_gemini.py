
from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL


def test_gemini_api():
    try:
        print("Connecting to Google Gemini API...")

        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.interactions.create(
            model=GEMINI_MODEL,
            input="Introduce NEXUS AI in one sentence."
        )

        print("\n" + "=" * 50)
        print("GEMINI API CONNECTION SUCCESSFUL!")
        print("=" * 50)

        print("\nGemini Response:")
        print(response.output_text)

    except Exception as error:
        print("\nGEMINI API CONNECTION FAILED!")
        print("Error:", error)


if __name__ == "__main__":
    test_gemini_api()
