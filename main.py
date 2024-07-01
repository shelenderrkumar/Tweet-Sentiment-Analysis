"""
    Import necessary libraries and modules:

    1. FastAPI for building REST API, HTTPException for error handling
    2. Pydantic for data validation and settings management
    3. SQLite3 for database operations
    4. Pandas for handling bulk insert operations with dataframes
    5. Custom model for sentiment analysis prediction

"""


from fastapi import FastAPI
from app.routers.sentiment_router import router as sentiment_router

app = FastAPI()
app.include_router(sentiment_router, prefix="/sentiment", tags=["Sentiment"])

