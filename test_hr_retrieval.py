from database.auth import authenticate_user
from modules.vector_store import search_documents

username = input("Username: ")
password = input("Password: ")

user = authenticate_user(username, password)

if not user:
    print("Login failed.")
    raise SystemExit

question = "What is the annual leave entitlement for employees?"

results = search_documents(
    question,
    top_k=5,
    user_role=user["role"],
    category="hr"
)

print("\nHR POLICY SEARCH RESULTS")
print("=" * 40)

if not results:
    print("No relevant information found.")

for result in results:
    print("\nDocument:", result["metadata"]["source"])
    print("Content:", result["text"])
    print("Distance:", result["distance"])