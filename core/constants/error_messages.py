"""
Error Messages Constants
"""


class ErrorMessages:
    """Error message constants"""

    # Validation Errors
    REQUIRED_FIELD = "This field is required"
    INVALID_EMAIL = "Invalid email format"
    INVALID_PASSWORD = "Password must be at least 8 characters"
    PASSWORD_MISMATCH = "Passwords do not match"

    # Authentication Errors
    INVALID_CREDENTIALS = "Invalid username or password"
    ACCOUNT_LOCKED = "Account is locked. Please contact support"
    SESSION_EXPIRED = "Your session has expired. Please login again"
    UNAUTHORIZED_ACCESS = "You are not authorized to access this resource"

    # API Errors
    API_TIMEOUT = "API request timed out"
    API_CONNECTION_ERROR = "Failed to connect to API server"
    INVALID_JSON = "Invalid JSON format"
    SCHEMA_VALIDATION_FAILED = "JSON schema validation failed"

    # Element Errors
    ELEMENT_NOT_FOUND = "Element not found: {selector}"
    ELEMENT_NOT_VISIBLE = "Element not visible: {selector}"
    ELEMENT_NOT_CLICKABLE = "Element not clickable: {selector}"

    # File Errors
    FILE_NOT_FOUND = "File not found: {file_path}"
    FILE_READ_ERROR = "Error reading file: {file_path}"
    FILE_WRITE_ERROR = "Error writing file: {file_path}"