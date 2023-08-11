"""Authorization API."""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies.auth import get_auth_service
from app.api.exceptions.auth import Unauthorized
from app.api.schemes.auth import Token
from app.core.auth import AuthService, create_user_access_token

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token')
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> Token:
    """Verify user and return access token.

    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends): Auth data.
        service (Annotated[AuthService, Depends]): Auth service.

    Raises:
        Unauthorized: If user is not authorized or token is invalid.

    Returns:
        Token: JWT access token.
    """
    user = await service.authorize_user(form_data.username, form_data.password)
    if not user:
        raise Unauthorized()

    access_token = create_user_access_token(uid=user.uid)
    # `bearer` is a type of access token
    return Token(access_token=access_token, token_type='bearer')  # noqa: S106
