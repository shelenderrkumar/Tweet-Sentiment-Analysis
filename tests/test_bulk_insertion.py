import pytest

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_bulk_insertion():
    file_path = "sample.csv"
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "text/csv")}
        response = client.post("/bulk_insertion", files=files)
        assert response.status_code == 200
        assert response.json() == {"message": "Bulk insert completed successfully."}
