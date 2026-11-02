
from database.auth import create_user, init_db


def setup():

    init_db()

    print("=" * 45)
    print("NEXUS AI - USER ACCOUNT SETUP")
    print("=" * 45)

    username = input("Enter username: ").strip()

    # Temporary visible password input for testing
    password = input("Enter password (minimum 8 characters): ")

    confirm_password = input("Confirm password: ")

    if password != confirm_password:
        print("\nPasswords do not match.")
        return

    print("\nSelect user role:")
    print("1. Administrator")
    print("2. Standard User")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        role = "admin"

    elif choice == "2":
        role = "standard"

    else:
        print("\nInvalid role selection.")
        return

    try:

        create_user(
            username=username,
            password=password,
            role=role
        )

        print("\n" + "=" * 45)
        print("USER ACCOUNT CREATED SUCCESSFULLY!")
        print("=" * 45)

        print("Username:", username)
        print("Role:", role)

    except ValueError as error:

        print("\nACCOUNT CREATION FAILED!")
        print("Error:", error)


if __name__ == "__main__":
    setup()
