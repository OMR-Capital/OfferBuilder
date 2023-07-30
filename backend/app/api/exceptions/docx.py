"""Exceptions for docx files."""

from http import HTTPStatus

from fastapi import HTTPException


class FailConvertToPDF(HTTPException):
    """Raised when the offer template file is bad."""

    def __init__(self, details: str = '') -> None:
        """Initialize the exception.

        Args:
            details (str): Exception details.
        """
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

        self.detail = 'Failed to convert to PDF'
        if details:
            self.detail += ': {details}'.format(details=details)
