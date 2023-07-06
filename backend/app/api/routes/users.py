"""Users API.

Contains CRUD operations for users.
"""

from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.api.schemes.users import (UserCreate, UserListResponse, UserOut,
                                   UserPasswordResponse, UserResponse,
                                   UserUpdate)
from app.core.security import generate_password, get_password_hash
from app.core.users import generate_uid
from app.db.user import UserInDB

router = APIRouter(prefix='/users', tags=['users'])


user_not_found = HTTPException(
    status_code=HTTPStatus.NOT_FOUND,
    detail='User not found',
)


@router.get('/')
async def get_users() -> UserListResponse:
    """Get all users.

    Returns:
        UserListResponse: List of users.
    """
    db_user = await UserInDB.get_all()
    users = [UserOut(**user.dict()) for user in db_user]
    return UserListResponse(users=users)


@router.get('/{uid}')
async def get_user(uid: str) -> UserResponse:
    """Get user by id.

    Args:
        uid (str): User id.

    Raises:
        user_not_found: Return 404 if user not found.

    Returns:
        UserResponse: User object.
    """
    db_user = await UserInDB.get_or_none(uid)
    if not db_user:
        raise user_not_found

    return UserResponse(user=UserOut(**db_user.dict()))


@router.post('/')
async def create_user(user: UserCreate) -> UserPasswordResponse:
    """Create user.

    Password and user id are generated automatically.
    See `app.core.users.generate_uid` and `app.core.security.get_password_hash`
    for more details.

    Args:
        user (UserCreate): User name and role.

    Returns:
        UserPasswordResponse: Created user object and generated password.
    """
    password = generate_password()
    password_hash = get_password_hash(password)
    uid = generate_uid()

    db_user = UserInDB(
        uid=uid,
        name=user.name,
        password_hash=password_hash,
        role=user.role,
    )
    await db_user.save()

    return UserPasswordResponse(
        user=UserOut(**db_user.dict()),
        password=password,
    )


@router.put('/{uid}')
async def update_user(uid: str, user: UserUpdate) -> UserResponse:
    """Update user.

    Args:
        uid (str): User id.
        user (UserUpdate): User name and role. None values are ignored.

    Raises:
        user_not_found: Return 404 if user not found.

    Returns:
        UserResponse: Updated user object.
    """
    db_user = await UserInDB.get_or_none(uid)
    if not db_user:
        raise user_not_found

    db_user.name = user.name or db_user.name
    db_user.role = user.role or db_user.role
    await db_user.save()

    return UserResponse(user=UserOut(**db_user.dict()))


@router.patch('/{uid}')
async def update_user_password(uid: str) -> UserPasswordResponse:
    """Generate new password for user.

    Args:
        uid (str): User id.

    Raises:
        user_not_found: Return 404 if user not found.

    Returns:
        UserPasswordResponse: User object and new password.
    """
    db_user = await UserInDB.get_or_none(uid)
    if not db_user:
        raise user_not_found

    password = generate_password()
    db_user.password_hash = get_password_hash(password)
    await db_user.save()

    return UserPasswordResponse(
        user=UserOut(**db_user.dict()),
        password=password,
    )


@router.delete('/{uid}')
async def delete_user(uid: str) -> UserResponse:
    """Delete user.

    Args:
        uid (str): User id.

    Raises:
        user_not_found: Return 404 if user not found.

    Returns:
        UserResponse: Deleted user object.
    """
    db_user = await UserInDB.get_or_none(uid)
    if not db_user:
        raise user_not_found

    await db_user.delete()

    return UserResponse(user=UserOut(**db_user.dict()))
