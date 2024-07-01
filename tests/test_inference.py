import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_inference():
    item = {"comment_id": "1", "comment_description": "This is great!"}
    response = client.post("/inference", json=item)
    assert response.status_code == 200
    assert "sentiment" in response.json()
