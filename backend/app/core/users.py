"""Utilities for users."""

from secrets import choice
from string import ascii_letters
from typing import Optional

from jose import JWTError

from app.core.auth import (
    generate_password,
    get_access_token_payload,
    get_password_hash,
)
from app.db.user import UserInDB
from app.models.user import User, UserRole


def generate_uid() -> str:
    """Generate user id.

    Returns:
        str: User id.
    """
    return ''.join(choice(ascii_letters) for _ in range(8))


async def get_authorized_user(token: str) -> Optional[User]:
    """Get current user from JWT token.

    Args:
        token (str): JWT token from oauth2 scheme.

    Raises:
        JWTError: If token is invalid

    Returns:
        Optional[User]: User instance if found, None otherwise.
    """
    try:
        payload = get_access_token_payload(token)
    except JWTError as exc:
        # Explicitly raise Unauthorized exception
        raise exc

    uid: Optional[str] = payload.get('sub')
    if uid is None:
        return None

    db_user = await UserInDB.get_or_none(uid)
    if db_user is None:
        return None

    return User(**db_user.dict())


async def get_verified_admin(user: User) -> Optional[User]:
    """Return user, verified to be admin.

    Args:
        user (User): Current user.

    Returns:
        Optional[User]: Admin user if it is admin, None otherwise.
    """
    if user.role not in {UserRole.admin, UserRole.superuser}:
        return None

    return user


class UserNotFoundError(Exception):
    """User not found."""


class LoginAlreadyExistsError(Exception):
    """Login already exists."""


class UsersService(object):
    """Users service.

    Provides methods for users management.
    """

    async def get_users(self) -> list[User]:
        """Get all users.

        Returns:
            list[User]: List of users.
        """
        db_users = await UserInDB.get_all()
        return [User(**db_user.dict()) for db_user in db_users]

    async def get_user(self, uid: str) -> User:
        """Get user by id.

        Args:
            uid (str): User id.

        Raises:
            UserNotFoundError: If user not found.

        Returns:
            User: User object if found, None otherwise.
        """
        db_user = await UserInDB.get_or_none(uid)
        if db_user is None:
            raise UserNotFoundError()

        return User(**db_user.dict())

    async def create_user(
        self,
        name: str,
        role: UserRole,
    ) -> tuple[User, str]:
        """Create user.

        Args:
            name (str): User name.
            role (UserRole): User role.

        Returns:
            tuple[User, str]: Created user and generated password.
        """
        password = generate_password()
        password_hash = get_password_hash(password)
        uid = generate_uid()

        db_user = UserInDB(
            uid=uid,
            login=uid,
            name=name,
            password_hash=password_hash,
            role=role,
        )
        await db_user.save()

        return User(**db_user.dict()), password

    async def update_user(
        self,
        uid: str,
        name: Optional[str] = None,
        login: Optional[str] = None,
        role: Optional[UserRole] = None,
    ) -> User:
        """Update user.

        Args:
            uid (str): User id.
            name (Optional[str], optional): User name. Defaults to None.
            login (Optional[str], optional): User login. Defaults to None.
            role (Optional[UserRole], optional): User role. Defaults to None.

        Raises:
            UserNotFoundError: If user not found.
            LoginAlreadyExistsError: If login already exists.

        Returns:
            User: Updated user.
        """
        db_user = await UserInDB.get_or_none(uid)
        if db_user is None:
            raise UserNotFoundError()

        db_user.name = name or db_user.name
        db_user.role = role or db_user.role

        if login:
            if not await self._check_login(login):
                raise LoginAlreadyExistsError()

            db_user.login = login

        await db_user.save()

        return User(**db_user.dict())

    async def update_user_password(self, uid: str) -> tuple[User, str]:
        """Update user password.

        Args:
            uid (str): User id.

        Raises:
            UserNotFoundError: If user not found.

        Returns:
            tuple[User, str]: Updated user and generated password.
        """
        db_user = await UserInDB.get_or_none(uid)
        if db_user is None:
            raise UserNotFoundError()

        password = generate_password()
        db_user.password_hash = get_password_hash(password)
        await db_user.save()

        return User(**db_user.dict()), password

    async def delete_user(self, uid: str) -> User:
        """Delete user.

        Args:
            uid (str): User id.

        Raises:
            UserNotFoundError: If user not found.

        Returns:
            User: Deleted user.
        """
        db_user = await UserInDB.get_or_none(uid)
        if db_user is None:
            raise UserNotFoundError()

        await db_user.delete()

        return User(**db_user.dict())

    async def _check_login(self, login: str) -> bool:
        """Check if login is already taken.

        Args:
            login (str): Login to check.

        Returns:
            bool: True if login is already taken, False otherwise.
        """
        # ODetaM queries are not typed properly, so we need to use ignore
        users_with_same_login = await UserInDB.query(UserInDB.login == login)
        return not bool(users_with_same_login)
