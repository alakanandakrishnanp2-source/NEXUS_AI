
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path("database/nexus.db")


def initialize_audit_log():
    """Create the audit log table if it does not exist."""

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                document_name TEXT,
                category TEXT,
                access_level TEXT,
                timestamp TEXT NOT NULL,
                status TEXT NOT NULL,
                details TEXT
            )
        """)

        connection.commit()


def record_activity(
    username,
    action,
    document_name=None,
    category=None,
    access_level=None,
    status="SUCCESS",
    details=None
):
    """Record an application activity."""

    initialize_audit_log()

    timestamp = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            INSERT INTO audit_logs (
                username,
                action,
                document_name,
                category,
                access_level,
                timestamp,
                status,
                details
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username,
            action,
            document_name,
            category,
            access_level,
            timestamp,
            status,
            details
        ))

        connection.commit()


def get_audit_logs(limit=100):
    """Retrieve recent audit log entries."""

    initialize_audit_log()

    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute("""
            SELECT *
            FROM audit_logs
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        return [dict(row) for row in rows]
