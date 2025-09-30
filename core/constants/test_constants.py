"""
Test Constants
"""


class TestConstants:
    """Test specific constants"""

    # Test Data
    VALID_USERNAME = "testuser@example.com"
    VALID_PASSWORD = "Test@123"
    INVALID_USERNAME = "invalid@example.com"
    INVALID_PASSWORD = "wrong_password"

    # Error Messages
    LOGIN_ERROR_MESSAGE = "Invalid credentials"
    REQUIRED_FIELD_ERROR = "This field is required"

    # Success Messages
    LOGIN_SUCCESS_MESSAGE = "Login successful"
    REGISTRATION_SUCCESS_MESSAGE = "Registration successful"

    # Timeouts
    SHORT_TIMEOUT = 5
    MEDIUM_TIMEOUT = 15
    LONG_TIMEOUT = 30

    # Retry
    MAX_RETRY_ATTEMPTS = 3
    RETRY_DELAY = 2