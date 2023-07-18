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
