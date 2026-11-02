from database.auth import authenticate_user
from modules.advisor_router import route_question


print("=" * 50)
print("NEXUS AI - AUTOMATIC ADVISOR ROUTING TEST")
print("=" * 50)

username = input("Username: ")
password = input("Password: ")

user = authenticate_user(username, password)

if not user:
    print("Login failed.")
    raise SystemExit


questions = [
    "Calculate the company's net profit and profit margin.",
    "How many annual leave days are employees entitled to?",
    "Give me an overview of the company."
]


for question in questions:

    print("\n" + "=" * 50)
    print("QUESTION:", question)

    try:
        result = route_question(
            question=question,
            user=user
        )

        print("\nSELECTED ADVISOR:", result["advisor"].upper())

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")
        for source in result["sources"]:
            print("-", source)

        if result.get("metrics"):
            print("\nFINANCIAL METRICS:")
            for key, value in result["metrics"].items():
                print(f"{key}: {value}")

    except Exception as error:
        print("Error:", error)