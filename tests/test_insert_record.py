import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_insert_record():
    item = {
        "comment_id": "1",
        "campaign_id": "1",
        "comment_description": "This is a test comment.",
        "sentiment": "positive",
    }
    response = client.post("/insert", json=item)
    assert response.status_code == 200
    assert response.json() == {"message": "Record inserted successfully."}
