"""User model."""


from enum import Enum

from pydantic import BaseModel


class UserRole(Enum):
    """User roles enumeration."""

    # Admin can manage users and application configuration
    admin = 'admin'

    # Employee can create offers
    employee = 'employee'


class User(BaseModel):
    """User representation in business logic."""

    # Model id from database
    uid: str

    # Full name
    name: str

    # Password. Password is stored as it is, without hashing
    # because db security is enough for this project
    password: str

    # User role
    role: UserRole
