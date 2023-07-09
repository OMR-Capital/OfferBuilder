"""Agents API exceptions."""


from http import HTTPStatus

from fastapi import HTTPException


class AgentNotFound(HTTPException):
    """Raised when the agent is not found."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.status_code = HTTPStatus.NOT_FOUND
        self.detail = 'Agent not found'
