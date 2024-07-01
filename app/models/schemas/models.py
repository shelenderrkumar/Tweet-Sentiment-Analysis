from pydantic import BaseModel


# Model for sentiment items, used for both predictions and insertions
class SentimentItem(BaseModel):
    comment_id: str
    campaign_id: str
    comment_description: str
    sentiment: str = None


# Model for updating sentiment records, similar to SentimentItem but without optional sentiment
class UpdateItem(BaseModel):
    comment_id: str
    campaign_id: str
    comment_description: str
    sentiment: str
