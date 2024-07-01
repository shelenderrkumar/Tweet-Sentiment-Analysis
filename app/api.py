from fastapi import APIRouter
from app.routers.sentiment_router import router as sentiment_router


router = APIRouter()

router.include_router(sentiment_router, prefix="/sentiment", tags=["Sentiment"])
