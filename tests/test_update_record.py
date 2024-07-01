import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_update_record():
    item = {
        "comment_id": "1",
        "campaign_id": "2",
        "comment_description": "This is an updated comment.",
        "sentiment": "neutral",
    }
    response = client.put("/update", json=item)
    assert response.status_code == 200
    assert response.json() == {"message": "Record updated successfully."}
