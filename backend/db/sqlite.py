import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any

# Database file in data/ directory at project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "tutor.db"

# Ensure data directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

_conn: Optional[sqlite3.Connection] = None

def get_conn() -> sqlite3.Connection:
    """Get or create database connection."""
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
    return _conn

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS tutor_sessions (
        id TEXT PRIMARY KEY,
        state TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
    )""")

    conn.commit()
