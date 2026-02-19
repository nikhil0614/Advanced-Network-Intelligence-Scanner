import sqlite3
import json
from datetime import datetime

def init_db():
    conn = sqlite3.connect("scan_history.db")
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
    conn = sqlite3.connect("scan_history.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO scans (target, result, timestamp) VALUES (?, ?, ?)",
        (target, json.dumps(result), datetime.now().isoformat())
    )

    conn.commit()
    conn.close()
