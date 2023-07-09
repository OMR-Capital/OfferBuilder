"""Works API exceptions."""


from http import HTTPStatus

from fastapi import HTTPException


class WorkNotFound(HTTPException):
    """Raised when the work is not found."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.NOT_FOUND
        self.detail = 'Work not found'
