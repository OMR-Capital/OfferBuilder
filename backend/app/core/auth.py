"""Auth  functions and utilities."""

from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import Any, Optional

from deta import Base
from jose import jwt
from passlib.context import CryptContext

from app.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
    ROOT_LOGIN,
    ROOT_PASSWORD,
)
from app.core.deta import serialize_model
from app.models.user import User, UserRole

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

ALGORITHM = 'HS256'


def create_user_access_token(
    uid: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create access JWT token for user auth.

    Args:
        uid (str): User id. Will be used as JWT subject.
        expires_delta (timedelta, optional): \
            Expires time. Defaults to ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: JWT token.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        )

    token_data = {'exp': expire, 'sub': uid}
    return jwt.encode(token_data, JWT_SECRET_KEY, algorithm=ALGORITHM)


def get_access_token_payload(token: str) -> dict[str, Any]:
    """Get access token payload.

    Args:
        token (str): JWT token.

    Returns:
        dict[str, Any]: Token payload.
    """
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])


def generate_password(length: int = 8) -> str:
    """Generate random password.

    Password is generated with secrets.token_urlsafe().

    Args:
        length (int): Password length. Defaults to 4.

    Returns:
        str: Password.
    """
    return token_urlsafe(length)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password hash.

    Args:
        plain_password (str): Password to verify.
        hashed_password (str): Hashed password.

    Returns:
        bool: True if password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Get password hash with bcrypt HS256.

    Args:
        password (str): Password to hash.

    Returns:
        str: Hashed password.
    """
    return pwd_context.hash(password)


class BadCredentialsError(Exception):
    """Bad credentials error."""


class AuthService(object):
    """Auth service.

    Provides methods for user authorization.
    """

    def __init__(self) -> None:
        """Initialize auth service."""
        self.base = Base('users')

    async def authorize_user(self, login: str, password: str) -> User:
        """Verify user credentials.

        New root user will be created and returned if user is root.

        Args:
            login (str): User login.
            password (str): User password.

        Raises:
            BadCredentialsError: If credentials are invalid.

        Returns:
            User: User instance if credentials are valid.
        """
        root_user = await self._register_root_user()
        if login == ROOT_LOGIN and password == ROOT_PASSWORD:
            return root_user

        users_with_login = self.base.fetch({'login': login}).items
        if not users_with_login:
            raise BadCredentialsError()

        user = User(**users_with_login[0])

        if not verify_password(password, user.password_hash):
            raise BadCredentialsError()

        return user

    async def _register_root_user(self) -> User:
        """Register root user.

        If root user already exists, do nothing.

        See ROOT_LOGIN and ROOT_PASSWORD in Spacefile.

        Returns:
            User: User instance.
        """
        user = User(
            uid=ROOT_LOGIN,
            login=ROOT_LOGIN,
            name='Root',
            role=UserRole.superuser,
            password_hash=get_password_hash(ROOT_PASSWORD),
        )
        self.base.put(serialize_model(user), user.uid)

        return User(**user.dict())
