import sqlite3
from fastapi import HTTPException

# Database connection string, pointing to a SQLite database on the local file system
DATABASE_URL = "C:/sqlite/database_shelender"

def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE_URL)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
