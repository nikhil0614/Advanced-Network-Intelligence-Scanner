import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "scan_history.db"


def get_connection():
    return sqlite3.connect(str(DB_PATH), timeout=10)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            result TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_scan(target, result):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO scans (target, result, timestamp) VALUES (?, ?, ?)",
        (target, json.dumps(result), datetime.now().isoformat())
    )

    conn.commit()
    conn.close()


def clear_scans():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            result TEXT,
            timestamp TEXT
        )
        """
    )
    cursor.execute("SELECT COUNT(*) FROM scans")
    deleted_count = cursor.fetchone()[0]

    cursor.execute("DELETE FROM scans")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='scans'")

    conn.commit()
    conn.close()
    return deleted_count
