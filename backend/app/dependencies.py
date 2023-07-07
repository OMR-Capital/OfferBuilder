"""Application dependencies."""


from typing import Annotated, Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.core.auth import get_access_token_payload
from app.db.user import UserInDB
from app.exceptions import AdminRightsRequired, Unauthorized
from app.models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
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


async def get_admin(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Get user verified as admin.

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
