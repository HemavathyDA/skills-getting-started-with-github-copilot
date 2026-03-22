"""
Unit tests for activity management business logic.

Tests use the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data
- Act: Execute the logic being tested
- Assert: Verify the result matches expected behavior
"""

import pytest


class TestActivityValidation:
    """Unit tests for activity validation logic"""
    
    def test_activity_exists_check(self, sample_activities):
        """
        Test checking if an activity exists.
        
        Given: A dictionary of activities
        When: Checking if an activity name exists
        Then: Correct boolean value is returned
        """
        # Arrange
        activity_name = "Chess Club"
        nonexistent_activity = "NonExistent Club"
        
        # Act & Assert
        assert activity_name in sample_activities
        assert nonexistent_activity not in sample_activities
    
    def test_activity_has_required_fields(self, sample_activities):
        """
        Test that activities have all required fields.
        
        Given: Sample activities data
        When: Inspecting an activity
        Then: All required fields are present
        """
        # Arrange
        activity = sample_activities["Chess Club"]
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act & Assert
        for field in required_fields:
            assert field in activity
            assert activity[field] is not None


class TestParticipantManagement:
    """Unit tests for participant addition and removal logic"""
    
    def test_add_participant_to_activity(self, sample_activities):
        """
        Test adding a new participant to an activity.
        
        Given: Activity with existing participants
        When: Adding a new participant
        Then: Participant is added and count increases
        """
        # Arrange
        activity = sample_activities["Chess Club"]
        initial_count = len(activity["participants"])
        new_email = "newstudent@mergington.edu"
        
        # Act
        activity["participants"].append(new_email)
        
        # Assert
        assert len(activity["participants"]) == initial_count + 1
        assert new_email in activity["participants"]
    
    def test_remove_participant_from_activity(self, sample_activities):
        """
        Test removing a participant from an activity.
        
        Given: Activity with existing participants
        When: Removing an existing participant
        Then: Participant is removed and count decreases
        """
        # Arrange
        activity = sample_activities["Chess Club"]
        initial_count = len(activity["participants"])
        email_to_remove = "michael@mergington.edu"
        
        # Act
        activity["participants"].remove(email_to_remove)
        
        # Assert
        assert len(activity["participants"]) == initial_count - 1
        assert email_to_remove not in activity["participants"]
    
    def test_duplicate_participant_check(self, sample_activities):
        """
        Test checking if a participant is already registered.
        
        Given: Activity with some participants
        When: Checking if participant exists
        Then: Correct result is returned
        """
        # Arrange
        activity = sample_activities["Chess Club"]
        existing_email = "michael@mergington.edu"
        new_email = "newstudent@mergington.edu"
        
        # Act & Assert
        assert existing_email in activity["participants"]
        assert new_email not in activity["participants"]
    
    def test_participant_list_isolated_between_activities(self, sample_activities):
        """
        Test that participant lists are isolated between activities.
        
        Given: Multiple activities with different participants
        When: Adding participant to one activity
        Then: Other activities' participant lists are unchanged
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity1 = sample_activities["Chess Club"]
        activity2 = sample_activities["Programming Class"]
        initial_prog_count = len(activity2["participants"])
        
        # Act
        activity1["participants"].append(email)
        
        # Assert
        assert email in activity1["participants"]
        assert email not in activity2["participants"]
        assert len(activity2["participants"]) == initial_prog_count


class TestParticipantLimitLogic:
    """Unit tests for participant limit enforcement"""
    
    def test_activity_has_max_participants_field(self, sample_activities):
        """
        Test that activities have max_participants defined.
        
        Given: Sample activities data
        When: Checking max_participants field
        Then: Field is present and is a positive integer
        """
        # Arrange
        activity = sample_activities["Chess Club"]
        
        # Act & Assert
        assert "max_participants" in activity
        assert isinstance(activity["max_participants"], int)
        assert activity["max_participants"] > 0
    
    def test_current_participants_count(self, sample_activities):
        """
        Test counting current participants in an activity.
        
        Given: Activity with known participants
        When: Counting participants
        Then: Correct count is returned
        """
        # Arrange
        activity = sample_activities["Chess Club"]
        expected_count = 2
        
        # Act
        current_count = len(activity["participants"])
        
        # Assert
        assert current_count == expected_count
    
    def test_space_available_calculation(self, sample_activities):
        """
        Test calculating available space in an activity.
        
        Given: Activity with participants and max limit
        When: Calculating available space
        Then: Correct available space is returned
        """
        # Arrange
        activity = sample_activities["Chess Club"]
        max_participants = activity["max_participants"]
        current_participants = len(activity["participants"])
        expected_available = max_participants - current_participants
        
        # Act
        available_space = max_participants - len(activity["participants"])
        
        # Assert
        assert available_space == expected_available
        assert available_space > 0
    
    def test_can_add_participant_when_space_available(self, sample_activities):
        """
        Test checking if participant can be added when space is available.
        
        Given: Activity with available space
        When: Checking if space exists
        Then: True is returned
        """
        # Arrange
        activity = sample_activities["Chess Club"]
        is_full = len(activity["participants"]) >= activity["max_participants"]
        
        # Act & Assert
        assert not is_full


class TestEmailValidation:
    """Unit tests for email validation logic"""
    
    def test_email_format_contains_at_symbol(self):
        """
        Test that valid emails contain @ symbol.
        
        Given: Email strings
        When: Checking if they are valid
        Then: Valid emails have @ symbol, invalid ones don't
        """
        # Arrange
        valid_email = "michael@mergington.edu"
        invalid_email = "michael.mergington.edu"
        
        # Act & Assert
        assert "@" in valid_email
        assert "@" not in invalid_email
    
    def test_sample_emails_are_valid_format(self, sample_activities):
        """
        Test that sample activity emails are in valid format.
        
        Given: Sample activities with participants
        When: Inspecting participant emails
        Then: All emails contain required format elements
        """
        # Arrange
        email_domain = "mergington.edu"
        
        # Act & Assert
        for activity_name, activity_data in sample_activities.items():
            for email in activity_data["participants"]:
                assert "@" in email
                assert email_domain in email


class TestStateConsistency:
    """Unit tests for maintaining state consistency"""
    
    def test_participant_not_duplicated_after_signup(self, sample_activities):
        """
        Test that participant appears only once after signup.
        
        Given: Activity with participants
        When: Adding a participant that doesn't exist
        Then: Participant appears exactly once
        """
        # Arrange
        activity = sample_activities["Chess Club"]
        email = "newstudent@mergington.edu"
        
        # Act
        activity["participants"].append(email)
        count = activity["participants"].count(email)
        
        # Assert
        assert count == 1
    
    def test_activity_structure_maintained_after_changes(self, sample_activities):
        """
        Test that activity structure remains valid after modifications.
        
        Given: Activity data
        When: Modifying participants list
        Then: All required fields remain present
        """
        # Arrange
        activity = sample_activities["Chess Club"]
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        activity["participants"].append("newstudent@mergington.edu")
        
        # Assert
        for field in required_fields:
            assert field in activity
    
    def test_participant_removal_doesnt_corrupt_list(self, sample_activities):
        """
        Test that removing participant maintains list integrity.
        
        Given: Activity with multiple participants
        When: Removing one participant
        Then: List remains valid and other participants intact
        """
        # Arrange
        activity = sample_activities["Chess Club"]
        email_to_remove = "michael@mergington.edu"
        other_email = "daniel@mergington.edu"
        initial_count = len(activity["participants"])
        
        # Act
        activity["participants"].remove(email_to_remove)
        
        # Assert
        assert len(activity["participants"]) == initial_count - 1
        assert isinstance(activity["participants"], list)
        assert other_email in activity["participants"]
