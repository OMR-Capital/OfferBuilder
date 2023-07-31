"""User model.

Users is a part of authorization system.
Them also used to sign offers.
"""


from enum import Enum

from pydantic import BaseModel


class UserRole(Enum):
    """User roles enumeration."""

    # Admin can manage users and application configuration
    admin = 'admin'

    # Employee can create offers
    employee = 'employee'

    # Superuser has developer rights
    superuser = 'superuser'


class User(BaseModel):
    """User representation in business logic."""

    # User id. Used as key in database
    uid: str

    # Login
    login: str

    # Full name
    name: str

    # Hashed password. See `app.core.security.get_password_hash`
    password_hash: str

    # User role
    role: UserRole
