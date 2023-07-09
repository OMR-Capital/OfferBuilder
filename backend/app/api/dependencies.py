"""API dependencies."""


from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.api.exceptions.auth import AdminRightsRequired, Unauthorized
from app.core import users
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    """Get current user from JWT token.

    See `app.core.users.get_current_user` for details.

    Args:
        token (str): JWT token from oauth2 scheme.

    Raises:
        Unauthorized: If token is invalid or user is not found.

    Returns:
        User: User instance.
    """
    try:
        user = await users.get_authorized_user(token)
    except JWTError:
        raise Unauthorized()

    if user is None:
        raise Unauthorized()

    return user


async def get_admin(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Get user verified as admin.

    See `app.core.users.get_admin` for details.

    Args:
        user (User): Current user.

    Raises:
        AdminRightsRequired: If user is not admin.

    Returns:
        User: Admin user.
    """
    admin = await users.get_verified_admin(user)
    if admin is None:
        raise AdminRightsRequired()

    return admin
