"""Auth  functions and utilities."""

from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import Any, Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY
from app.db.user import UserInDB
from app.models.user import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def authenticate_user(uid: str, password: str) -> Optional[User]:
    """Verify user credentials.

    Args:
        uid (str): User id.
        password (str): User password.

    Returns:
        Optional[User]: User instance if credentials are valid.
    """
    db_user = await UserInDB.get_or_none(uid)
    if not db_user:
        return None

    if not verify_password(password, db_user.password_hash):
        return None

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