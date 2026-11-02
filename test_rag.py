
from database.auth import authenticate_user
from modules.rag_engine import ask_nexus


print("=" * 50)
print("NEXUS AI - ROLE-BASED RAG TEST")
print("=" * 50)

username = input("Enter username: ")
password = input("Enter password: ")

user = authenticate_user(username, password)

if not user:
    print("Login failed. Please check your credentials.")
else:
    print("\nLogin successful!")
    print("Role:", user["role"])

    question = input("\nAsk NEXUS AI: ")

    try:
        result = ask_nexus(
            question=question,
            user=user
        )

        print("\nNEXUS AI RESPONSE")
        print("-" * 40)
        print(result["answer"])

        print("\nSources:")
        for source in result["sources"]:
            print("-", source)

    except Exception as error:
        print("\nTEST FAILED:", error)
