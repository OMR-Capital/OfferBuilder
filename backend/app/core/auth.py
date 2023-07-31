"""Auth  functions and utilities."""

from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import Any, Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
    ROOT_LOGIN,
    ROOT_PASSWORD,
)
from app.db.user import UserInDB
from app.models.user import User, UserRole

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def authorize_user(login: str, password: str) -> Optional[User]:
    """Verify user credentials.

    Args:
        login (str): User login.
        password (str): User password.

    Returns:
        Optional[User]: User instance if credentials are valid.
    """
    root_user = await register_root_user()
    if login == ROOT_LOGIN and password == ROOT_PASSWORD:
        return root_user

    # ODetaM queries are not typed properly, so we need to use ignore
    users_with_login = await UserInDB.query(
        UserInDB.login == login,  # type: ignore
    )
    if not users_with_login:
        return None

    db_user = users_with_login[0]

    if not verify_password(password, db_user.password_hash):
        return None

    return User(**db_user.dict())


async def register_root_user() -> User:
    """Register root user.

    If root user already exists, do nothing.

    See ROOT_LOGIN and ROOT_PASSWORD in Spacefile.

    Returns:
        User: User instance.
    """
    db_user = UserInDB(
        uid=ROOT_LOGIN,
        login=ROOT_LOGIN,
        name='Root',
        role=UserRole.superuser,
        password_hash=get_password_hash(ROOT_PASSWORD),
    )
    await db_user.save()

    return User(**db_user.dict())


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


def generate_password(length: int = 4) -> str:
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
