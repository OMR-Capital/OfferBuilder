"""Authorization and permissions exceptions."""


from http import HTTPStatus

from fastapi import HTTPException


class Unauthorized(HTTPException):
    """Raised when the user is not authorized or the token is invalid."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.UNAUTHORIZED
        self.detail = 'Incorrect username or password'
        self.headers = {'WWW-Authenticate': 'Bearer'}


class AdminRightsRequired(HTTPException):
    """Raised when the user is not authorized to access a resource."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.FORBIDDEN
        self.detail = 'Admin rights are required.'
