"""Authentication API."""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.schemes.auth import Token
from app.core.auth import authenticate_user, create_user_access_token
from app.exceptions import Unauthorized

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token')
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Verify user and return access token.

    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends): Auth data.

    Raises:
        Unauthorized: If user is not authorized or token is invalid.

    Returns:
        Token: JWT access token.
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise Unauthorized()

    access_token = create_user_access_token(uid=user.uid)
    # `bearer` is a type of access token
    return Token(access_token=access_token, token_type='bearer')  # noqa: S106
