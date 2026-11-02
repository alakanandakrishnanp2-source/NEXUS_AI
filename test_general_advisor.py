
from database.auth import authenticate_user
from modules.rag_engine import ask_nexus

print("NEXUS AI - GENERAL ASSISTANT TEST")

username = input("Username: ")
password = input("Password: ")

user = authenticate_user(username, password)

if not user:
    print("Login failed.")
    raise SystemExit

question = input("Ask a general question: ")

print("\nRetrieving documents and generating answer...\n", flush=True)

try:
    result = ask_nexus(question, user)

    print("ANSWER:")
    print(result["answer"])

    print("\nSOURCES:")
    for source in result["sources"]:
        print("-", source)

    print("\nTEST COMPLETED")

except Exception as error:
    print("TEST FAILED:", repr(error))
