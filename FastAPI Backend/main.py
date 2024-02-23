
"""
    Import necessary libraries and modules:

    1. FastAPI for building REST API, HTTPException for error handling
    2. Pydantic for data validation and settings management
    3. SQLite3 for database operations
    4. Pandas for handling bulk insert operations with dataframes
    5. Custom model for sentiment analysis prediction

"""

import sqlite3
import pandas as pd

from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import List
from model import predict_sentiment 


# Initialize FastAPI app
app = FastAPI()

# Database connection string, pointing to a SQLite database on the local file system
DATABASE_URL = "C:/sqlite/database_shelender"

# Pydantic models are defined for data validation and serialization.
# Model for sentiment items, used for both predictions and insertions
class SentimentItem(BaseModel):
    comment_id: str
    campaign_id: str
    description: str
    sentiment: str = None  # Optional, as it might not be provided for insert

# Model for updating sentiment records, similar to SentimentItem but without optional sentiment
class UpdateItem(BaseModel):
    comment_id: str
    campaign_id: str
    description: str
    sentiment: str


#Helper function to establish a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn


# Endpoint for predicting the sentiment of a single comment
@app.post("/predict/")
async def predict(item: SentimentItem):
    sentiment = predict_sentiment(item.description)
    return {"comment_id": item.comment_id, "sentiment": sentiment}


# Endpoint for inserting a new sentiment record into the database
@app.post("/insert/")
async def insert(item: SentimentItem):
    conn = get_db_connection()
    # SQL INSERT command is executed to add the new record
    conn.execute("INSERT INTO sentiment_analysis (comment_id, campaign_id, description, sentiment) VALUES (?, ?, ?, ?)",
                 (item.comment_id, item.campaign_id, item.description, item.sentiment))
    conn.commit()
    conn.close() # Database connection is closed
    return {"message": "Record inserted successfully."}


# Endpoint for deleting a sentiment record by its comment I
@app.delete("/delete/{comment_id}")
async def delete(comment_id: str):
    conn = get_db_connection()
    # SQL DELETE command is executed to remove the specified record
    conn.execute("DELETE FROM sentiment_analysis WHERE comment_id = ?", (comment_id,))
    conn.commit()
    # If no records were deleted, the comment ID was not found; 404 error is raised
    if conn.total_changes == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Record not found")
    conn.close()
    return {"message": "Record deleted successfully."}


# Endpoint for updating an existing sentiment record
@app.put("/update/")
async def update(item: UpdateItem):
    conn = get_db_connection()
    # SQL UPDATE command is executed to modify the specified record
    conn.execute("UPDATE sentiment_analysis SET campaign_id = ?, description = ?, sentiment = ? WHERE comment_id = ?",
                 (item.campaign_id, item.description, item.sentiment, item.comment_id))
    conn.commit()
    # Here we check if any records were actually updated
    if conn.total_changes == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Record not found")
    conn.close()
    return {"message": "Record updated successfully."}


# Endpoint for inserting a bulk sentiment record into the database
@app.post("/bulk_insert/")
async def bulk_insert(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    df['sentiment'] = df['comment_description'].apply(predict_sentiment)
    conn = get_db_connection()
    df.to_sql('sentiment_analysis', conn, if_exists='append', index=False)
    conn.close()
    return {"message": "Bulk insert completed successfully."}

