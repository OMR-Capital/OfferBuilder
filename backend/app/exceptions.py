"""Extensions."""


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


class UserNotFound(HTTPException):
    """Raised when the user is not found."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.NOT_FOUND
        self.detail = 'User not found'


class CompanyNotFound(HTTPException):
    """Raised when the company is not found."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.NOT_FOUND
        self.detail = 'Company not found'


class WasteNotFound(HTTPException):
    """Raised when the waste is not found."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.NOT_FOUND
        self.detail = 'Waste not found'
