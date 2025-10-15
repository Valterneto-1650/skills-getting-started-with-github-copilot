import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    """Create a test client for our FastAPI app"""
    return TestClient(app)

@pytest.fixture
def sample_activity_data():
    """Sample activity data for testing"""
    return {
        "Test Activity": {
            "description": "Test activity for unit tests",
            "schedule": "Mondays, 2:00 PM - 3:00 PM",
            "max_participants": 5,
            "participants": []
        }
    }