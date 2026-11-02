
import sqlite3
import hashlib
import secrets
import hmac

from pathlib import Path


# --------------------------------------------------
# 1. DATABASE CONFIGURATION
# --------------------------------------------------

DB_PATH = Path("database/nexus.db")

HASH_ITERATIONS = 310000


# --------------------------------------------------
# 2. DATABASE CONNECTION
# --------------------------------------------------

def get_connection():
    """Create a connection to the SQLite database."""

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


# --------------------------------------------------
# 3. INITIALIZE USER TABLE
# --------------------------------------------------

def init_db():
    """Create the users table if it does not exist."""

    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                role TEXT NOT NULL
                    CHECK(role IN ('admin', 'standard')),
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()

    finally:
        connection.close()


# --------------------------------------------------
# 4. HASH PASSWORD
# --------------------------------------------------

def hash_password(password, salt=None):
    """Hash a password securely using PBKDF2."""

    if salt is None:
        salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        HASH_ITERATIONS
    )

    return salt.hex(), password_hash.hex()


# --------------------------------------------------
# 5. CREATE USER
# --------------------------------------------------

def create_user(username, password, role):
    """Create a new administrator or standard user."""

    username = username.strip()

    if not username:
        raise ValueError("Username cannot be empty.")

    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")

    if role not in ("admin", "standard"):
        raise ValueError("Role must be admin or standard.")

    init_db()

    salt, password_hash = hash_password(password)

    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO users (
                username,
                password_hash,
                salt,
                role
            )
            VALUES (?, ?, ?, ?)
        """, (username, password_hash, salt, role))

        connection.commit()

        return True

    except sqlite3.IntegrityError:
        raise ValueError("This username already exists.")

    finally:
        connection.close()


# --------------------------------------------------
# 6. AUTHENTICATE USER
# --------------------------------------------------

def authenticate_user(username, password):
    """Verify login credentials and return user information."""

    init_db()

    connection = get_connection()

    try:
        user = connection.execute("""
            SELECT *
            FROM users
            WHERE username = ?
            AND is_active = 1
        """, (username.strip(),)).fetchone()

        if user is None:
            return None

        salt = bytes.fromhex(user["salt"])

        _, entered_hash = hash_password(
            password,
            salt
        )

        if hmac.compare_digest(
            entered_hash,
            user["password_hash"]
        ):

            return {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"]
            }

        return None

    finally:
        connection.close()


# --------------------------------------------------
# 7. CHECK USER ROLE
# --------------------------------------------------

def is_admin(user):
    """Check whether the logged-in user is an administrator."""

    return user is not None and user.get("role") == "admin"
