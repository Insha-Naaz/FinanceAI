# core/database/connection.py

import sqlite3
from config.settings import DB_PATH  # import DB path from settings

def get_db_connection():
    """Return a connection to the SQLite database based on current environment."""
    return sqlite3.connect(DB_PATH)
