"""Schemes of auth API."""


from pydantic import BaseModel


class Token(BaseModel):
    """Token scheme."""

    access_token: str
    token_type: str
