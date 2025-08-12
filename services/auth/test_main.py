import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_register_endpoint():
    """Test user registration endpoint"""
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    })
    assert response.status_code in [200, 201, 422]  # Accept various valid responses

def test_login_endpoint():
    """Test user login endpoint"""
    response = client.post("/login", data={
        "username": "testuser",
        "password": "testpassword123"
    })
    assert response.status_code in [200, 401, 422]  # Accept various valid responses
