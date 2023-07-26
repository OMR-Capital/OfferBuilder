"""Offers API exceptions."""

from http import HTTPStatus

from fastapi import HTTPException


class OfferNotFound(HTTPException):
    """Raised when the offer is not found."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.NOT_FOUND
        self.detail = 'Offer not found'


class OfferUploadFailed(HTTPException):
    """Raised when the offer upload failed."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.detail = 'Offer upload failed'


class BadOfferFile(HTTPException):
    """Raised when the offer file is bad."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.BAD_REQUEST
        self.detail = 'Bad offer file'
