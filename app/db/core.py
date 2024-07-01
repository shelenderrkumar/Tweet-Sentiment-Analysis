import sqlite3
from fastapi import HTTPException


# Database connection string, pointing to a SQLite database on the local file system
DATABASE_URL = "C:/sqlite/database_shelender"


def get_db_connection():
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance.

    Args:
      table_handle:
        An open smalltable.Table instance.

    Returns:
      A dict mapping keys to the corresponding table row data
      
    Raises:
      IOError: An error occurred accessing the smalltable.
    """

    try:
        conn = sqlite3.connect(DATABASE_URL)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
