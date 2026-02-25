import sqlite3
import json
from datetime import datetime
from pathlib import Path
import os
import shutil

BASE_DIR = Path(__file__).resolve().parent
# Keep DB inside project to align with sandbox and avoid permission clashes.
DB_DIR = BASE_DIR / "data_user"
DB_DIR.mkdir(parents=True, exist_ok=True)

LEGACY_DB_ROOT = BASE_DIR / "scan_history.db"
LEGACY_DB_DATA = BASE_DIR / "data" / "scan_history.db"
LEGACY_DB_CWD = Path.cwd() / "scan_history.db"

# mutable global that always points to the currently writable DB
DB_PATH = DB_DIR / "scan_history.db"
CANDIDATE_DB_PATHS = {DB_PATH, LEGACY_DB_ROOT, LEGACY_DB_DATA, LEGACY_DB_CWD}


def ensure_db_writable(path: Path):
    if path.exists():
        try:
            os.chmod(path, 0o666)
        except Exception:
            pass


def _choose_db_path():
    global DB_PATH

    preferred = DB_DIR / "scan_history.db"

    def writable(p: Path) -> bool:
        return p.exists() and os.access(p, os.W_OK)

    # Try preferred path first
    if preferred.exists():
        ensure_db_writable(preferred)
        if writable(preferred):
            DB_PATH = preferred
            return DB_PATH

    # Try legacy locations (root/data/cwd)
    for legacy in (LEGACY_DB_DATA, LEGACY_DB_ROOT, LEGACY_DB_CWD):
        if legacy.exists():
            ensure_db_writable(legacy)
            try:
                DB_DIR.mkdir(parents=True, exist_ok=True)
                shutil.copy2(legacy, preferred)
                os.chmod(preferred, 0o666)
                DB_PATH = preferred
                return DB_PATH
            except Exception:
                # If copy fails, but legacy is writable, use it directly
                if writable(legacy):
                    DB_PATH = legacy
                    return DB_PATH

    # If preferred not present, create new
    DB_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH = preferred
    return DB_PATH


def get_connection():
    path = _choose_db_path()
    ensure_db_writable(path)
    return sqlite3.connect(str(path), timeout=10)

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
    # Ensure target directory exists and db recreated in primary location
    DB_DIR.mkdir(parents=True, exist_ok=True)
    init_db()
    return removed
