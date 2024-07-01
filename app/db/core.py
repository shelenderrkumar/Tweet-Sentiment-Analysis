import sqlite3
from fastapi import HTTPException


DATABASE_URL = "C:/sqlite/database_shelender"


def get_db_connection():
    """Fetches connection from the database.

    Returns:
      Commection for the database to perform crud opeartions.

    Raises:
      HTTPException: An exception is raised if connection is not fetched.
    """

    try:
        conn = sqlite3.connect(DATABASE_URL)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Database connection error: {str(e)}"
        )
