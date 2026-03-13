import sqlite3
from config import DB_NAME

def get_connection() -> sqlite3.Connection:
    """
    Підключення до SQLite + вмикаємо foreign keys.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn