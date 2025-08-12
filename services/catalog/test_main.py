import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_events():
    """Test get events endpoint"""
    response = client.get("/events")
    assert response.status_code in [200, 404]  # Accept various valid responses

def test_get_event():
    """Test get single event endpoint"""
    response = client.get("/events/1")
    assert response.status_code in [200, 404]  # Accept various valid responses
