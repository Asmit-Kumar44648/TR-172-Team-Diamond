import pytest
from fastapi.testclient import TestClient
import io
from ..main import app

client = TestClient(app)

# 1. Test Auth logic
def test_unauthenticated_request_returns_401():
    response = client.get("/v1/scenes/upload") # Changed to a valid but protected endpoint
    assert response.status_code == 401
    assert "Missing authentication" in response.json()["detail"]

# 5. Upload Endpoint (Basic Schema Check)
def test_upload_missing_file():
    response = client.post("/v1/scenes/upload")
    # Expected 422 Unprocessable Entity due to missing required field
    assert response.status_code == 422

# Simple health check
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "ok"
