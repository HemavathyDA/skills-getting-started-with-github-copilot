"""
Integration tests for FastAPI activity management endpoints.

Tests use the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and fixtures
- Act: Execute the endpoint being tested
- Assert: Verify the result matches expected behavior
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all activities with correct structure.
        
        Given: API server is running
        When: Client makes GET request to /activities
        Then: Response contains all activities with 200 status
        """
        # Arrange
        expected_activity_count = 3  # Based on sample_activities fixture
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(data) == expected_activity_count
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
    
    def test_get_activities_contains_correct_fields(self, client):
        """
        Test that each activity has required fields.
        
        Given: API server with activities data
        When: Client retrieves activities
        Then: Each activity contains description, schedule, max_participants, and participants
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert set(activity_data.keys()) == required_fields
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)
    
    def test_get_activities_participants_list_correct(self, client):
        """
        Test that the participants list matches expected values.
        
        Given: Sample activities with known participant lists
        When: Client retrieves activities
        Then: Participant lists contain expected email addresses
        """
        # Arrange
        expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
        expected_gym_participants = ["john@mergington.edu", "olivia@mergington.edu"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert data["Chess Club"]["participants"] == expected_chess_participants
        assert data["Gym Class"]["participants"] == expected_gym_participants


class TestSignUp:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_successful(self, client):
        """
        Test successful signup for an activity.
        
        Given: Valid activity name and email
        When: Client POSTs to signup endpoint
        Then: Response is 200 and participant is added to activity
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]
    
    def test_signup_duplicate_participant_returns_400(self, client):
        """
        Test that duplicate signup returns 400 error.
        
        Given: Student already signed up for an activity
        When: Client attempts to signup again
        Then: Response is 400 with error detail
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in sample_activities
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_nonexistent_activity_returns_404(self, client):
        """
        Test that signup to non-existent activity returns 404.
        
        Given: Activity name that does not exist
        When: Client attempts to signup
        Then: Response is 404 with error detail
        """
        # Arrange
        activity_name = "Non-existent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_multiple_activities_same_student(self, client):
        """
        Test that a student can signup for multiple activities.
        
        Given: Student signed up for one activity
        When: Student signs up for another activity
        Then: Student appears in both activities
        """
        # Arrange
        student_email = "newstudent@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # Act
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": student_email}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert student_email in activities_data[activity1]["participants"]
        assert student_email in activities_data[activity2]["participants"]


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_successful(self, client):
        """
        Test successful unregistration from an activity.
        
        Given: Student currently registered for an activity
        When: Client makes DELETE request to unregister
        Then: Response is 200 and participant is removed
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in sample_activities
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity_name]["participants"]
    
    def test_unregister_not_registered_returns_400(self, client):
        """
        Test that unregistering non-registered student returns 400.
        
        Given: Student not registered for an activity
        When: Client attempts to unregister
        Then: Response is 400 with error detail
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notstudent@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]
    
    def test_unregister_nonexistent_activity_returns_404(self, client):
        """
        Test that unregistering from non-existent activity returns 404.
        
        Given: Activity name that does not exist
        When: Client attempts to unregister
        Then: Response is 404 with error detail
        """
        # Arrange
        activity_name = "Non-existent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_maintains_other_participants(self, client):
        """
        Test that unregistering one student doesn't affect others.
        
        Given: Activity with multiple participants
        When: One participant unregisters
        Then: Other participants remain in the activity
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        email_to_keep = "daniel@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove}
        )
        
        # Assert
        assert response.status_code == 200
        
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email_to_remove not in activities_data[activity_name]["participants"]
        assert email_to_keep in activities_data[activity_name]["participants"]
