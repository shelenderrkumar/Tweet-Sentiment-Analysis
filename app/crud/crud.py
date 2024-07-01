import sqlite3
import pandas as pd

from fastapi import HTTPException
from ..db.core import get_db_connection
from app.utils.inference import predict_sentiment


async def inference(item):
    """Predicts sentiment for a tweeet.

    Args:
      item: A single element containing text and comment_id.

    Returns:
      Label predicted for the tweet text by the model

    Raises:
      HTTPException: Prediction error if model is unable to predict.
    """

    try:
        sentiment = predict_sentiment(item.comment_description)
        return {"comment_id": item.comment_id, "sentiment": sentiment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


async def insert_record(item):
    """Inserts new sentiment record into the database

    Args:
      Sentiment Record to be inserted in the database.

    Returns:
      A dict containing the message indicating that record is inserted.

    Raises:
      HTTPException: An error if record is not inserted.
    """

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO sentiment_analysis (comment_id, campaign_id, comment_description, sentiment) VALUES (?, ?, ?, ?)",
            (
                item.comment_id,
                item.campaign_id,
                item.comment_description,
                item.sentiment,
            ),
        )
        conn.commit()
    except:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e
    finally:
        conn.close()
    return {"message": "Record inserted successfully."}


async def delete_record(comment_id: str):
    """Deletes a sentiment record by its comment id

    Args:
      Comment ID of the sentiment record to be deleted from database

    Returns:
      A dict containing the message indicating that record is deleted.

    Raises:
      HTTPException: An error if record is not deleted successfully.
    """

    conn = get_db_connection()
    try:
        conn.execute(
            "DELETE FROM sentiment_analysis WHERE comment_id = ?", (comment_id,)
        )
        conn.commit()
        if conn.total_changes == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Record not found")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Delete error: {str(e)}")
    finally:
        conn.close()
    return {"message": "Record deleted successfully."}


async def update_record(item):
    """Updates a existing sentiment record

    Args:
      Sentiment Record to be inserted in the database:

    Returns:
      A dict containing the message indicating that record is updated.

    Raises:
      HTTPException: An error if record is not updated successfully.
    """

    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE sentiment_analysis SET campaign_id = ?, comment_description = ?, sentiment = ? WHERE comment_id = ?",
            (
                item.campaign_id,
                item.comment_description,
                item.sentiment,
                item.comment_id,
            ),
        )
        conn.commit()
        if conn.total_changes == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Record not found")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Update error: {str(e)}")
    finally:
        conn.close()
    return {"message": "Record updated successfully."}


async def bulk_insertion(file):
    """Predicts sentiment and insertion of records in bulk.

    Args:
      File: containing the records.

    Returns:
      A dict containing the message indicating that record is inserted.

    Raises:
      ValueError: An error if record is not inserted successfully.
    """

    try:
        df = pd.read_csv(file.file)
        df["sentiment"] = df["comment_description"].apply(predict_sentiment)
        print(df)

    except UnicodeDecodeError as e:
        raise HTTPException(
            status_code=400,
            detail="Could not decode CSV. Please check the file encoding.",
        )

    conn = get_db_connection()

    try:
        df.to_sql("sentiment_analysis", conn, if_exists="append", index=False)
    except ValueError as e:
        raise HTTPException(
            status_code=500, detail=f"Bulk insert schema error: {str(e)}"
        )
    except UnicodeDecodeError as e:
        raise HTTPException(
            status_code=400,
            detail="Could not decode CSV. Please check the file encoding.",
        )
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Bulk insert error: {str(e)}")
    finally:
        conn.close()
    return {"message": "Bulk insert completed successfully."}
