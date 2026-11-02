
from database.auth import authenticate_user, is_admin


print("=" * 45)
print("NEXUS AI - LOGIN TEST")
print("=" * 45)

username = input("Username: ")
password = input("Password: ")

user = authenticate_user(username, password)

if user:

    print("\nLOGIN SUCCESSFUL!")
    print("Username:", user["username"])
    print("Role:", user["role"])

    if is_admin(user):
        print("Access Level: Administrator")
    else:
        print("Access Level: Standard User")

else:

    print("\nLOGIN FAILED!")
    print("Invalid username or password.")
