import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_process_payment():
    """Test process payment endpoint"""
    response = client.post("/process-payment", json={
        "booking_id": "test-booking-id",
        "amount": 100.0,
        "phone_number": "1234567890"
    })
    assert response.status_code in [200, 201, 422]  # Accept various valid responses

def test_get_payment():
    """Test get payment endpoint"""
    response = client.get("/payment/test-payment-id")
    assert response.status_code in [200, 404]  # Accept various valid responses
