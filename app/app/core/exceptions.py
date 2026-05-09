class AppException(Exception):
    """Base exception class for the application."""
    pass

class NotFoundException(AppException):
    """Exception raised when an entity is not found."""
    pass

class ValidationException(AppException):
    """Exception raised for validation errors."""
    pass