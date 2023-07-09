"""Offer templates API exceptions."""


from http import HTTPStatus

from fastapi import HTTPException


class OfferTemplateNotFound(HTTPException):
    """Raised when the offer template is not found."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.NOT_FOUND
        self.detail = 'Offer template not found'


class OfferTemplateUploadFailed(HTTPException):
    """Raised when the offer template upload failed."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.detail = 'Offer template upload failed'


class IncorrectOfferTemplateFile(HTTPException):
    """Raised when the offer template file is not valid docx."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.BAD_REQUEST
        self.detail = 'Only docx files are allowed.'
