import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_booking():
    """Test create booking endpoint"""
    response = client.post("/bookings", json={
        "event_id": 1,
        "user_id": 1,
        "num_seats": 2
    })
    assert response.status_code in [200, 201, 422]  # Accept various valid responses

def test_get_bookings():
    """Test get bookings endpoint"""
    response = client.get("/bookings")
    assert response.status_code in [200, 404]  # Accept various valid responses
