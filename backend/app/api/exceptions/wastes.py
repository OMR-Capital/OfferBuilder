"""Wastes API exceptions."""


from http import HTTPStatus

from fastapi import HTTPException


class WasteNotFound(HTTPException):
    """Raised when the waste is not found."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.NOT_FOUND
        self.detail = 'Waste not found'
