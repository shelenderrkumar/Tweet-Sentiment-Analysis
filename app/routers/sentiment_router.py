from fastapi import APIRouter, HTTPException, File, UploadFile
from ..models import SentimentItem, UpdateItem
from ..database import get_db_connection
from ..utils.inference import predict_sentiment

router = APIRouter()


# Endpoint for predicting the sentiment of a single comment
@router.post("/predict/")
async def predict(item: SentimentItem):
    try:
        sentiment = predict_sentiment(item.comment_description)
        return {"comment_id": item.comment_id, "sentiment": sentiment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


# Endpoint for inserting a new sentiment record into the database
@router.post("/insert/")
async def insert(item: SentimentItem):
    conn = get_db_connection()
    try:
        # SQL INSERT command is executed to add the new record
        conn.execute("INSERT INTO sentiment_analysis (comment_id, campaign_id, comment_description, sentiment) VALUES (?, ?, ?, ?)",
                    (item.comment_id, item.campaign_id, item.comment_description, item.sentiment))
        conn.commit()
    except:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e
    finally:
        conn.close() # Database connection is closed
    return {"message": "Record inserted successfully."}


# Endpoint for deleting a sentiment record by its comment I
@router.delete("/delete/{comment_id}")
async def delete(comment_id: str):
    conn = get_db_connection()
    try:
        # SQL DELETE command is executed to remove the specified record
        conn.execute("DELETE FROM sentiment_analysis WHERE comment_id = ?", (comment_id,))
        conn.commit()
        # If no records were deleted, the comment ID was not found; 404 error is raised
        if conn.total_changes == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Record not found")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Delete error: {str(e)}")
    finally:
        conn.close()
    return {"message": "Record deleted successfully."}


# Endpoint for updating an existing sentiment record
@router.put("/update/")
async def update(item: UpdateItem):
    conn = get_db_connection()
    try:
        # SQL UPDATE command is executed to modify the specified record
        conn.execute("UPDATE sentiment_analysis SET campaign_id = ?, comment_description = ?, sentiment = ? WHERE comment_id = ?",
                    (item.campaign_id, item.comment_description, item.sentiment, item.comment_id))
        conn.commit()
        # Here we check if any records were actually updated
        if conn.total_changes == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Record not found")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Update error: {str(e)}")
    finally:
        conn.close()
    return {"message": "Record updated successfully."}


# Endpoint for inserting a bulk sentiment record into the database
@router.post("/bulk_insert/")
async def bulk_insert(file: UploadFile = File(...)):
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
    except ValueError as e:  # This might occur if there's a mismatch in DataFrame to SQL table schema
        raise HTTPException(status_code=500, detail=f"Bulk insert schema error: {str(e)}")
    except UnicodeDecodeError as e:
        raise HTTPException(status_code=400, detail="Could not decode CSV. Please check the file encoding.")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Bulk insert error: {str(e)}")
    finally:
        conn.close()
    return {"message": "Bulk insert completed successfully."}