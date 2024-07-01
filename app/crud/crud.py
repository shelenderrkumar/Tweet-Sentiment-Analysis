import sqlite3
import pandas as pd

from fastapi import HTTPException
from ..db.core import get_db_connection
from app.utils.inference import predict_sentiment


async def inference(
        item
    ) -> str:

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
        sentiment = predict_sentiment(item.comment_description)
        return {"comment_id": item.comment_id, "sentiment": sentiment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


# Endpoint for inserting a new sentiment record into the database
async def insert_record(
        item
    ):
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

    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO sentiment_analysis (comment_id, campaign_id, comment_description, sentiment) VALUES (?, ?, ?, ?)",
                    (item.comment_id, item.campaign_id, item.comment_description, item.sentiment))
        conn.commit()
    except:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e
    finally:
        conn.close() 
    return {"message": "Record inserted successfully."}


# Endpoint for deleting a sentiment record by its comment I
async def delete_record(
        comment_id: str
    ):
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

    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM sentiment_analysis WHERE comment_id = ?", (comment_id,))
        conn.commit()
        if conn.total_changes == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Record not found")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Delete error: {str(e)}")
    finally:
        conn.close()
    return {"message": "Record deleted successfully."}


# Endpoint for updating an existing sentiment record
async def update_record(
        item
    ):
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

    conn = get_db_connection()
    try:
        conn.execute("UPDATE sentiment_analysis SET campaign_id = ?, comment_description = ?, sentiment = ? WHERE comment_id = ?",
                    (item.campaign_id, item.comment_description, item.sentiment, item.comment_id))
        conn.commit()
        if conn.total_changes == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Record not found")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Update error: {str(e)}")
    finally:
        conn.close()
    return {"message": "Record updated successfully."}


async def bulk_insertion(
        file
    ):
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
        df = pd.read_csv(file.file)
        print(df)
        df['sentiment'] = df['comment_description'].apply(predict_sentiment)
        print(df)

    except UnicodeDecodeError as e:
        raise HTTPException(status_code=400, detail="Could not decode CSV. Please check the file encoding.")
    
    conn = get_db_connection()

    try:
        df.to_sql('sentiment_analysis', conn, if_exists='append', index=False)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Bulk insert schema error: {str(e)}")
    except UnicodeDecodeError as e:
        raise HTTPException(status_code=400, detail="Could not decode CSV. Please check the file encoding.")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Bulk insert error: {str(e)}")
    finally:
        conn.close()
    return {"message": "Bulk insert completed successfully."}