"""Utilities for users."""

from secrets import choice
from string import ascii_letters
from typing import Optional

from jose import JWTError

from app.core.auth import get_access_token_payload
from app.db.user import UserInDB
from app.models.user import User, UserRole


def generate_uid() -> str:
    """Generate user id.

    Returns:
        str: User id.
    """
    return ''.join(choice(ascii_letters) for _ in range(8))


async def get_authorized_user(token: str) -> Optional[User]:
    """Get current user from JWT token.

    Args:
        token (str): JWT token from oauth2 scheme.

    Raises:
        JWTError: If token is invalid

    Returns:
        Optional[User]: User instance if found, None otherwise.
    """
    try:
        payload = get_access_token_payload(token)
    except JWTError as exc:
        # Explicitly raise Unauthorized exception
        raise exc

    uid: Optional[str] = payload.get('sub')
    if uid is None:
        return None

    db_user = await UserInDB.get_or_none(uid)
    if db_user is None:
        return None

    return User(**db_user.dict())


async def get_verified_admin(user: User) -> Optional[User]:
    """Return user, verified to be admin.

    Args:
        user (User): Current user.

    Returns:
        Optional[User]: Admin user if it is admin, None otherwise.
    """
    if user.role != UserRole.admin:
        return None

    return user


async def check_login(login: str) -> bool:
    """Check if login is already taken.

    Args:
        login (str): Login to check.

    Returns:
        bool: True if login is already taken, False otherwise.
    """
    # ODetaM queries are not typed properly, so we need to use ignore
    users_with_same_login = await UserInDB.query(
        UserInDB.login == login,  # type: ignore
    )
    return not bool(users_with_same_login)
