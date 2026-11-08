class AppException(Exception):
    """Base exception for application-level errors."""

class ResourceNotFoundError(AppException):
    """Raised when a requested resource does not exist."""

class AuthorizationError(AppException):
    """Raised when the user is not allowed to perform an action."""

class ValidationError(AppException):
    """Raised when business-level validation fails."""

class WorkflowExecutionError(AppException):
    """Raised when workflow execution fails."""

class DuplicateEmailError(AppException):
    """Raised when a user attempts to register an existing email."""
    def __init__(self, email: str):
        self.email = email
        super().__init__("Email already registered")