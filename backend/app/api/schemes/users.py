"""Schemes of users API."""

from pydantic import BaseModel

from app.models.user import UserRole


class CreateUser(BaseModel):
    """Create user scheme."""

    name: str
    password: str
    role: UserRole
