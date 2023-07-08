"""Users API.

Contains CRUD operations for users.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.schemes.users import (UserCreate, UserListResponse, UserOut,
                                   UserPasswordResponse, UserResponse,
                                   UserUpdate)
from app.core.auth import generate_password, get_password_hash
from app.core.users import generate_uid
from app.db.user import UserInDB
from app.api.dependencies import get_admin, get_current_user
from app.api.exceptions import AdminRightsRequired, UserNotFound
from app.models.user import User, UserRole

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/me')
async def get_my_user(
    user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    """Get current user.

    Args:
        user (User): Authorized user model.

    Returns:
        UserResponse: _description_
    """
    return UserResponse(user=UserOut(**user.dict()))


@router.get('/')
async def get_users(
    admin: Annotated[User, Depends(get_admin)],
) -> UserListResponse:
    """Get all users.

    Args:
        admin (User): Current user must be an admin.

    Returns:
        UserListResponse: List of users.
    """
    db_user = await UserInDB.get_all()
    users = [UserOut(**user.dict()) for user in db_user]
    return UserListResponse(users=users)


@router.get('/{uid}')
async def get_user(
    uid: str,
    user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    """Get user by id.

    If current user is not admin, only self info available.
    Admin can get any user.

    Args:
        uid (str): User id.
        user (User): Current user.

    Raises:
        UserNotFound: If user not found.
        AdminRightsRequired: \
            If non-admin user tries to get info about other user.

    Returns:
        UserResponse: User object.
    """
    if user.role != UserRole.admin and user.uid != uid:
        raise AdminRightsRequired()

    db_user = await UserInDB.get_or_none(uid)
    if not db_user:
        raise UserNotFound()

    return UserResponse(user=UserOut(**db_user.dict()))


@router.post('/')
async def create_user(
    user_data: UserCreate,
    admin: Annotated[User, Depends(get_admin)],
) -> UserPasswordResponse:
    """Create user.

    Password and user id are generated automatically.
    See `app.core.users.generate_uid` and `app.core.security.get_password_hash`
    for more details.

    Args:
        user_data (UserCreate): User name and role.
        admin (User): Current user must be an admin.

    Returns:
        UserPasswordResponse: Created user object and generated password.
    """
    password = generate_password()
    password_hash = get_password_hash(password)
    uid = generate_uid()

    db_user = UserInDB(
        uid=uid,
        name=user_data.name,
        password_hash=password_hash,
        role=user_data.role,
    )
    await db_user.save()

    return UserPasswordResponse(
        user=UserOut(**db_user.dict()),
        password=password,
    )


@router.put('/{uid}')
async def update_user(
    uid: str,
    user_data: UserUpdate,
    admin: Annotated[User, Depends(get_admin)],
) -> UserResponse:
    """Update user.

    Args:
        uid (str): User id.
        user_data (UserUpdate): User name and role. None values are ignored.
        admin (User): Current user must be an admin.

    Raises:
        UserNotFound: If user not found.

    Returns:
        UserResponse: Updated user object.
    """
    db_user = await UserInDB.get_or_none(uid)
    if not db_user:
        raise UserNotFound()

    db_user.name = user_data.name or db_user.name
    db_user.role = user_data.role or db_user.role
    await db_user.save()

    return UserResponse(user=UserOut(**db_user.dict()))


@router.patch('/{uid}')
async def update_user_password(
    uid: str,
    admin: Annotated[User, Depends(get_admin)],
) -> UserPasswordResponse:
    """Generate new password for user.

    Args:
        uid (str): User id.
        admin (User): Current user must be an admin.

    Raises:
        UserNotFound: If user not found.

    Returns:
        UserPasswordResponse: User object and new password.
    """
    db_user = await UserInDB.get_or_none(uid)
    if not db_user:
        raise UserNotFound()

    password = generate_password()
    db_user.password_hash = get_password_hash(password)
    await db_user.save()

    return UserPasswordResponse(
        user=UserOut(**db_user.dict()),
        password=password,
    )


@router.delete('/{uid}')
async def delete_user(
    uid: str,
    admin: Annotated[User, Depends(get_admin)],
) -> UserResponse:
    """Delete user.

    Args:
        uid (str): User id.
        admin (User): Current user must be an admin.

    Raises:
        UserNotFound: If user not found.

    Returns:
        UserResponse: Deleted user object.
    """
    db_user = await UserInDB.get_or_none(uid)
    if not db_user:
        raise UserNotFound()

    await db_user.delete()

    return UserResponse(user=UserOut(**db_user.dict()))
