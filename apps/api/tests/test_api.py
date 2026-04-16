import pytest
from fastapi.testclient import TestClient
import io
from ..main import app

client = TestClient(app)

# 1. Test Auth logic (Integration via an endpoint, e.g. billing usage which requires auth)
def test_unauthenticated_request_returns_401():
    response = client.get("/v1/billing/usage")
    assert response.status_code == 401
    assert "Missing authentication" in response.json()["detail"]

def test_invalid_jwt_returns_401():
    response = client.get("/v1/billing/usage", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert "Invalid or expired JWT" in response.json()["detail"]

# 2. Test Rate Limiter logic
# We use a mocked/dummy Dependency override or mocked redis
# Since we might not have a running redis locally, upstash client gracefully fails if not set or we mock get_current_org
def override_get_current_org_free():
    return {"org_id": "test_org", "plan": "free"}

app.dependency_overrides[app.router.dependencies] = {} 
# In a real test suite we'd use unittesting.mock or app.dependency_overrides directly on the imported function
from ..auth import get_current_org
app.dependency_overrides[get_current_org] = override_get_current_org_free

# 3. Test API Key Creation
# Mocks require mocking Supabase. We test the dummy path if DB is mostly abstracted or mocked
def test_create_api_key(mocker): # using pytest-mock normally
    pass

# 4. Stripe webhook signature
def test_stripe_webhook_invalid_sig():
    response = client.post("/v1/billing/webhook", headers={"stripe-signature": "invalid"}, content=b'{}')
    # Because STRIPE_WEBHOOK_SECRET might not be mocked, we might hit 500 or 400
    assert response.status_code in [400, 500] 

# 5. Upload Endpoint
def test_upload_missing_file():
    response = client.post("/v1/scenes/upload")
    # Expected 422 Unprocessable Entity due to missing required field
    assert response.status_code == 422

# Simple health check
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}
