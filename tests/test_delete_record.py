import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_delete_record():
    response = client.delete("/delete/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Record deleted successfully."}
