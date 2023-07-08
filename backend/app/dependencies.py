"""Application dependencies."""


from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

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

    Returns:
        User: User instance.
    """
    return await users.get_authorized_user(token)


async def get_admin(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Get user verified as admin.

    See `app.core.users.get_admin` for details.

    Args:
        user (User): Current user.

    Returns:
        User: Admin user.
    """
    return await users.verify_admin(user)
