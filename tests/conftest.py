"""
Pytest configuration and fixtures for FastAPI tests
"""

import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def test_app():
    """
    Fixture providing the FastAPI application instance.
    
    This fixture is used to create a fresh app instance for testing.
    """
    return app


@pytest.fixture
def client(test_app):
    """
    Fixture providing a TestClient for making HTTP requests to the app.
    
    The TestClient allows us to make test requests without running
    a live server, capturing requests and responses for assertions.
    """
    return TestClient(test_app)


@pytest.fixture
def sample_activities():
    """
    Fixture providing a copy of the sample activities data.
    
    Returns a fresh copy of the activities for each test to ensure
    test isolation and prevent cross-test pollution.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
    }


@pytest.fixture(autouse=True)
def reset_activities(sample_activities):
    """
    Fixture that resets the activities database before each test.
    
    This fixture automatically runs before each test (autouse=True)
    to ensure a consistent state and prevent test interdependencies.
    """
    # Clear existing activities
    activities.clear()
    
    # Reload sample data
    activities.update(sample_activities)
    
    yield
    
    # Cleanup after test
    activities.clear()
