
from database.auth import authenticate_user
from modules.finance_advisor import analyze_finances


print("=" * 50)
print("NEXUS AI - FINANCE ADVISOR TEST")
print("=" * 50)

username = input("Username: ")
password = input("Password: ")

user = authenticate_user(username, password)

if not user:
    print("Login failed.")
else:
    question = input(
        "\nAsk Finance Advisor: "
    )

    try:
        result = analyze_finances(
            question=question,
            user=user
        )

        print("\nFINANCIAL ANALYSIS")
        print("-" * 40)

        if result["metrics"]:
            for key, value in result["metrics"].items():
                print(f"{key}: {value}")

        print("\nAI ADVISOR:")
        print(result["answer"])

        print("\nSOURCES:")
        for source in result["sources"]:
            print("-", source)

    except Exception as error:
        print("Error:", error)

