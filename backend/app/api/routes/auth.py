"""Authentication API."""

from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.schemes.auth import Token
from app.core.auth import authenticate_user, create_user_access_token

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token')
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Verify user and return access token.

    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends): Auth data.

    Raises:
        HTTPException: Return 404 if user credentials are invalid.

    Returns:
        Token: JWT access token.
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = create_user_access_token(uid=user.uid)
    return Token(access_token=access_token, token_type='bearer')
