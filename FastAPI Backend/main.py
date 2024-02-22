from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import sqlite3
from typing import List
import pandas as pd
from model import predict_sentiment 

app = FastAPI()

DATABASE_URL = "sqlite:///C:/sqlite/database_shelender"


class SentimentItem(BaseModel):
    comment_id: str
    campaign_id: str
    description: str
    sentiment: str = None  # Optional, as it might not be provided for insert


class UpdateItem(BaseModel):
    comment_id: str
    campaign_id: str
    description: str
    sentiment: str


def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn


@app.post("/predict/")
async def predict(item: SentimentItem):
    sentiment = predict_sentiment(item.description)
    return {"comment_id": item.comment_id, "sentiment": sentiment}


@app.post("/insert/")
async def insert(item: SentimentItem):
    conn = get_db_connection()
    conn.execute("INSERT INTO sentiment_analysis (comment_id, campaign_id, description, sentiment) VALUES (?, ?, ?, ?)",
                 (item.comment_id, item.campaign_id, item.description, item.sentiment))
    conn.commit()
    conn.close()
    return {"message": "Record inserted successfully."}



@app.delete("/delete/{comment_id}")
async def delete(comment_id: str):
    conn = get_db_connection()
    conn.execute("DELETE FROM sentiment_analysis WHERE comment_id = ?", (comment_id,))
    conn.commit()
    if conn.total_changes == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Record not found")
    conn.close()
    return {"message": "Record deleted successfully."}



@app.put("/update/")
async def update(item: UpdateItem):
    conn = get_db_connection()
    conn.execute("UPDATE sentiment_analysis SET campaign_id = ?, description = ?, sentiment = ? WHERE comment_id = ?",
                 (item.campaign_id, item.description, item.sentiment, item.comment_id))
    conn.commit()
    if conn.total_changes == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Record not found")
    conn.close()
    return {"message": "Record updated successfully."}



@app.post("/bulk_insert/")
async def bulk_insert(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    df['sentiment'] = df['description'].apply(predict_sentiment)  # Assuming 'description' column exists
    conn = get_db_connection()
    df.to_sql('sentiment_analysis', conn, if_exists='append', index=False)
    conn.close()
    return {"message": "Bulk insert completed successfully."}

