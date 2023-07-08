"""Utilities for users."""

from secrets import choice
from string import ascii_letters
from typing import Optional

from jose import JWTError

from app.core.auth import get_access_token_payload
from app.db.user import UserInDB
from app.exceptions import AdminRightsRequired, Unauthorized
from app.models.user import User, UserRole


def generate_uid() -> str:
    """Generate user id.

    Returns:
        str: User id.
    """
    return ''.join(choice(ascii_letters) for _ in range(8))


async def get_authorized_user(token: str) -> User:
    """Get current user from JWT token.

    Args:
        token (str): JWT token from oauth2 scheme.

    Raises:
        Unauthorized: If token is invalid or user is not found.

    Returns:
        User: User instance.
    """
    try:
        payload = get_access_token_payload(token)
    except JWTError:
        raise Unauthorized()

    uid: Optional[str] = payload.get('sub')
    if uid is None:
        raise Unauthorized()

    db_user = await UserInDB.get_or_none(uid)
    if db_user is None:
        raise Unauthorized()

    return User(**db_user.dict())


async def verify_admin(user: User) -> User:
    """Verify that user is admin.

    Args:
        user (User): Current user.

    Raises:
        AdminRightsRequired: If user is not admin.

    Returns:
        User: Admin user.
    """
    if user.role != UserRole.admin:
        raise AdminRightsRequired()

    return user
