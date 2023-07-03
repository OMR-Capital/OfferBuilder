"""Users API.

Contains CRUD operations for users.
"""

from fastapi import APIRouter

from app.api.schemes.users import CreateUser
from app.models.user import User, UserRole

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/')
async def get_users() -> list[User]:
    """Get all users.

    Returns:
        List[User]: List of users.
    """
    return []


@router.get('/{user_id}')
async def get_user(uid: str) -> User:
    """Get user by id.

    Args:
        uid (str): User id.

    Returns:
        User: User object.
    """
    return User(uid=uid, name='John Doe', password=uid, role=UserRole.employee)


@router.post('/')
async def create_user(user: CreateUser) -> User:
    """Create user.

    Args:
        user (CreateUser): User data.

    Returns:
        User: Created user object.
    """
    return User(
        uid='1',
        name=user.name,
        password=user.password,
        role=user.role,
    )


@router.put('/{user_id}')
async def update_user(uid: str, user: CreateUser) -> User:
    """Update user.

    Args:
        uid (str): User id.
        user (CreateUser): User data.

    Returns:
        User: Updated user object.
    """
    return User(
        uid=uid,
        name=user.name,
        password=user.password,
        role=user.role,
    )


@router.delete('/{user_id}')
async def delete_user(uid: str) -> None:
    """Delete user.

    Args:
        uid (str): User id.
    """
