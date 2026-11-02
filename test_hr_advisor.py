from database.auth import authenticate_user
from modules.hr_advisor import analyze_hr_question


print("=" * 50)
print("NEXUS AI - HR ADVISOR TEST")
print("=" * 50)

username = input("Username: ")
password = input("Password: ")

user = authenticate_user(username, password)

if not user:
    print("Login failed.")
    raise SystemExit

question = input("\nAsk HR Advisor: ")

result = analyze_hr_question(
    question=question,
    user=user
)

print("\nHR ADVISOR RESPONSE")
print("-" * 40)

print(result["answer"])

print("\nSOURCES:")

for source in result["sources"]:
    print("-", source)