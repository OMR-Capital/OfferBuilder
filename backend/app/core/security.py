"""Security utilities."""

from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


ALGORITHM = 'HS256'


def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create access JWT token.

    Args:
        subject (Union[str, Any]): Token subject.
        expires_delta (timedelta, optional): Expires time. Defaults to None.

    Returns:
        str: JWT token.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    token_data = {'exp': expire, 'sub': str(subject)}
    return jwt.encode(token_data, JWT_SECRET_KEY, algorithm=ALGORITHM)


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
