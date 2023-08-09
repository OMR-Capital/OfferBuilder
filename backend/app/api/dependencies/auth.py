"""Auth dependencies."""


from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.api.exceptions.auth import Unauthorized
from app.api.exceptions.users import AdminRightsRequired
from app.core.users import get_authorized_user, get_verified_admin
from app.models.user import User

# Authorization form in Swagger UI doesn't work properly under Deta proxy
# So, we need to specify prefix manually
PROXY_PREFIX = '/api'
token_url = '{prefix}/auth/token'.format(prefix=PROXY_PREFIX)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)


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
        user = await get_authorized_user(token)
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
    admin = await get_verified_admin(user)
    if admin is None:
        raise AdminRightsRequired()

    return admin
