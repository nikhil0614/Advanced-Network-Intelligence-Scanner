import sqlite3
import json
from datetime import datetime
from pathlib import Path
import os
import shutil

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "data"
DB_DIR.mkdir(exist_ok=True)

LEGACY_DB = BASE_DIR / "scan_history.db"
DB_PATH = DB_DIR / "scan_history.db"
CANDIDATE_DB_PATHS = {DB_PATH, LEGACY_DB, Path.cwd() / "scan_history.db"}


def ensure_db_writable(path: Path):
    if path.exists():
        try:
            os.chmod(path, 0o666)
        except Exception:
            pass


def _migrate_legacy_db():
    if LEGACY_DB.exists() and not DB_PATH.exists():
        try:
            shutil.copy2(LEGACY_DB, DB_PATH)
            os.chmod(DB_PATH, 0o666)
        except Exception:
            pass


def get_connection():
    _migrate_legacy_db()
    ensure_db_writable(DB_PATH)
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
    try:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='scans'")
    except sqlite3.Error:
        # sqlite_sequence may not exist yet; clearing rows is enough.
        pass

    conn.commit()
    conn.close()
    return deleted_count


def get_scan_count():
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
    count = cursor.fetchone()[0]
    conn.close()
    return count


def hard_reset_database():
    # Reset to a fresh-clone state by removing any known DB file; fall back to drop if locked.
    removed = False
    for path in CANDIDATE_DB_PATHS:
        ensure_db_writable(path)
        try:
            if path.exists():
                path.unlink()
                removed = True
        except PermissionError:
            # If we cannot unlink (locked), drop table in that file instead.
            conn = sqlite3.connect(str(path), timeout=10)
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS scans")
            conn.commit()
            conn.close()
            removed = True
    init_db()
    return removed
