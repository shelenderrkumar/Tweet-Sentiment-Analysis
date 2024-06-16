from pydantic import BaseModel

# Pydantic models are defined for data validation and serialization.
# Model for sentiment items, used for both predictions and insertions
class SentimentItem(BaseModel):
    comment_id: str
    campaign_id: str
    comment_description: str
    sentiment: str = None  #Optional, as it might not be provided for insert

# Model for updating sentiment records, similar to SentimentItem but without optional sentiment
class UpdateItem(BaseModel):
    comment_id: str
    campaign_id: str
    comment_description: str
    sentiment: str
