"""
    Import necessary libraries and modules:

    1. FastAPI for building REST API, HTTPException for error handling
    2. Pydantic for data validation and settings management
    3. SQLite3 for database operations
    4. Pandas for handling bulk insert operations with dataframes
    5. Custom model for sentiment analysis prediction

"""
import uvicorn

from fastapi import FastAPI

from app.api import router as api_router

from app.core.events import create_start_app_handler, create_stop_app_handler

app = FastAPI()

app.include_router(api_router)

app.add_event_handler("startup", create_start_app_handler(app))
app.add_event_handler("shutdoen", create_stop_app_handler(app))

if __name__ = "__main__":
    uvicorn.run("main:app", host = "0.0.0.0". port = 8000, reload=True)

