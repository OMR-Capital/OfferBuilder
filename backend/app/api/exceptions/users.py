"""Users API exceptions."""


from http import HTTPStatus

from fastapi import HTTPException


class UserNotFound(HTTPException):
    """Raised when the user is not found."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.NOT_FOUND
        self.detail = 'User not found'


class LoginAlreadyExists(HTTPException):
    """Raised when the login already exists."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.CONFLICT
        self.detail = 'Login already exists'


class AdminRightsRequired(HTTPException):
    """Raised when the resource requires admin rights."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.FORBIDDEN
        self.detail = 'Admin rights are required.'


class AccessDenied(HTTPException):
    """Raised when the resource access is denied."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.FORBIDDEN
        self.detail = 'Access denied.'
