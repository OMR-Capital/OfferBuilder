"""Companies API exceptions."""


from http import HTTPStatus

from fastapi import HTTPException


class CompanyNotFound(HTTPException):
    """Raised when the company is not found."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.NOT_FOUND
        self.detail = 'Company not found'
