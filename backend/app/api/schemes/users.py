"""Schemes of users API."""

from typing import Optional

from pydantic import BaseModel

from app.models.user import UserRole


class UserOut(BaseModel):
    """Public user scheme."""

    uid: str
    login: str
    name: str
    role: UserRole


class UserCreate(BaseModel):
    """Create user scheme."""

    name: str
    role: UserRole


class UserUpdate(BaseModel):
    """Update user scheme."""

    login: Optional[str] = None
    name: Optional[str] = None
    role: Optional[UserRole] = None


class UserResponse(BaseModel):
    """User response scheme."""

    user: UserOut


class UserListResponse(BaseModel):
    """User list response scheme."""

    users: list[UserOut]


class UserPasswordResponse(BaseModel):
    """Password update response scheme."""

    user: UserOut
    password: str
