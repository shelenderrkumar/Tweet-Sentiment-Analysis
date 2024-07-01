import sqlite3

from fastapi import APIRouter, HTTPException, File, UploadFile
from ..models.models import SentimentItem, UpdateItem
from ..db.core import get_db_connection
from ..utils.inference import predict_sentiment
from ..crud.crud import inference, insert_record, delete_record, update_record, bulk_insertion


router = APIRouter(
    prefix="/setiment-router"
)


# Endpoint for predicting the sentiment of a single comment
@router.post("/predict/")
async def predict(
    item: SentimentItem
):
    return await inference(item)


# Endpoint for inserting a new sentiment record into the database
@router.post("/insert/")
async def insert(
    item: SentimentItem
):
    return await insert_record(item)


# Endpoint for deleting a sentiment record by its comment I
@router.delete("/delete/{comment_id}")
async def delete(
    comment_id: str
):
    return await delete_record(comment_id)


# Endpoint for updating an existing sentiment record
@router.put("/update/")
async def update(
    item: UpdateItem
):
    return await update_record(item)


# Endpoint for inserting a bulk sentiment record into the database
@router.post("/bulk_insert/")
async def bulk_insert(
    file: UploadFile = File(...)
):
    return await bulk_insertion(file)