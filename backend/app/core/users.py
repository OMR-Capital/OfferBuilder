"""Utilities for users."""

from secrets import choice
from string import ascii_letters
from typing import Optional

from deta import Base
from jose import JWTError

from app.core.auth import (
    generate_password,
    get_access_token_payload,
    get_password_hash,
)
from app.core.deta import serialize_model
from app.core.pagination import (
    PaginationParams,
    PaginationResponse,
    default_pagination,
)
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

    db_user = Base('users').get(uid)
    if db_user is None:
        return None

    return User(**db_user)


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

    def __init__(self) -> None:
        """Initialize users service."""
        self.base = Base('users')

    async def get_users(
        self,
        pagination: PaginationParams = default_pagination,
    ) -> PaginationResponse[User]:
        """Get all users.

        Args:
            pagination (PaginationParams): Pagination params.

        Returns:
            PaginationResponse[User]: Pagination response.
        """
        response = self.base.fetch(
            limit=pagination.limit,
            last=pagination.last,
        )
        users = [User(**db_user) for db_user in response.items]
        return PaginationResponse(
            items=users,
            last=response.last,
        )

    async def get_user(self, uid: str) -> User:
        """Get user by id.

        Args:
            uid (str): User id.

        Raises:
            UserNotFoundError: If user not found.

        Returns:
            User: User object if found, None otherwise.
        """
        db_user = self.base.get(uid)
        if db_user is None:
            raise UserNotFoundError()

        return User(**db_user)

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

        user = User(
            uid=uid,
            login=uid,
            name=name,
            password_hash=password_hash,
            role=role,
        )
        self.base.put(serialize_model(user), uid)

        return user, password

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
        db_user = self.base.get(uid)
        if db_user is None:
            raise UserNotFoundError()

        db_user['name'] = name or db_user['name']
        db_user['role'] = role or db_user['role']

        if login:
            if not await self._check_login(login):
                raise LoginAlreadyExistsError()

            db_user['login'] = login

        self.base.put(db_user, uid)

        return User(**db_user)

    async def update_user_password(self, uid: str) -> tuple[User, str]:
        """Update user password.

        Args:
            uid (str): User id.

        Raises:
            UserNotFoundError: If user not found.

        Returns:
            tuple[User, str]: Updated user and generated password.
        """
        db_user = self.base.get(uid)
        if db_user is None:
            raise UserNotFoundError()

        password = generate_password()
        db_user['password_hash'] = get_password_hash(password)
        self.base.put(db_user, uid)

        return User(**db_user), password

    async def delete_user(self, uid: str) -> User:
        """Delete user.

        Args:
            uid (str): User id.

        Raises:
            UserNotFoundError: If user not found.

        Returns:
            User: Deleted user.
        """
        db_user = self.base.get(uid)
        if db_user is None:
            raise UserNotFoundError()

        self.base.delete(uid)

        return User(**db_user)

    async def _check_login(self, login: str) -> bool:
        """Check if login is already taken.

        Args:
            login (str): Login to check.

        Returns:
            bool: True if login is already taken, False otherwise.
        """
        # ODetaM queries are not typed properly, so we need to use ignore
        users_with_same_login = self.base.fetch({'login': login}).items
        return not bool(users_with_same_login)
