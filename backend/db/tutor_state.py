import sqlite3, json
from datetime import datetime
from pathlib import Path
from .sqlite import DB_PATH

# Ensure data directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def save_state(session_id : str, state: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    INSERT OR REPLACE INTO tutor_sessions (id, state, updated_at)
    VALUES (?, ?, ?)""", (session_id, json.dumps(state), datetime.now()))

    conn.commit()
    conn.close()

def load_state(session_id: str) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT state FROM tutor_sessions WHERE id = ?", (session_id,))

    row = c.fetchone()
    conn.close()

    if row:
        return json.loads(row[0])
    return None

