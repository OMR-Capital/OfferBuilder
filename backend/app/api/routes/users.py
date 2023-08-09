"""Users API.

Contains CRUD operations for users.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_admin, get_current_user
from app.api.dependencies.users import get_users_service
from app.api.exceptions.users import LoginAlreadyExists, UserNotFound
from app.api.schemes.users import (
    MyUserUpdate,
    UserCreate,
    UserListResponse,
    UserOut,
    UserPasswordResponse,
    UserResponse,
    UserUpdate,
)
from app.core.users import (
    LoginAlreadyExistsError,
    UserNotFoundError,
    UsersService,
)
from app.models.user import User

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/me')
async def get_my_user(
    user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    """Get current user.

    Args:
        user (User): Authorized user model.

    Raises:
        UserNotFound: If user not found in database.

    Returns:
        UserResponse: _description_
    """
    return UserResponse(user=UserOut(**user.dict()))


@router.put('/me')
async def update_my_user(
    user_data: MyUserUpdate,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[UsersService, Depends(get_users_service)],
) -> UserResponse:
    """Update current user.

    Args:
        user_data (MyUserUpdate): User data. All fields are optional.
        user (User): Authorized user model.
        service (UsersService): Users service.

    Raises:
        UserNotFound: If user not found in database.
        LoginAlreadyExists: If login already exists.

    Returns:
        UserResponse: Updated user object.
    """
    try:
        user = await service.update_user(
            uid=user.uid,
            name=user_data.name,
            login=user_data.login,
        )
    except UserNotFoundError:
        raise UserNotFound()
    except LoginAlreadyExistsError:
        raise LoginAlreadyExists()

    return UserResponse(user=UserOut(**user.dict()))


@router.patch('/me/password')
async def update_my_user_password(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[UsersService, Depends(get_users_service)],
) -> UserPasswordResponse:
    """Generate new password for current user.

    Args:
        user (User): Authorized user model.
        service (UsersService): Users service.

    Raises:
        UserNotFound: If user not found in database.

    Returns:
        UserPasswordResponse: User object and new password.
    """
    try:
        user, password = await service.update_user_password(uid=user.uid)
    except UserNotFoundError:
        raise UserNotFound()

    return UserPasswordResponse(
        user=UserOut(**user.dict()),
        password=password,
    )


@router.get('/')
async def get_users(
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[UsersService, Depends(get_users_service)],
) -> UserListResponse:
    """Get all users.

    Args:
        admin (User): Current user must be an admin.
        service (UsersService): Users service.

    Raises:
        AdminRightsRequired: If current user is not an admin.

    Returns:
        UserListResponse: List of users.
    """
    users = await service.get_users()
    out_users = [UserOut(**user.dict()) for user in users]
    return UserListResponse(users=out_users)


@router.get('/{uid}')
async def get_user(
    uid: str,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[UsersService, Depends(get_users_service)],
) -> UserResponse:
    """Get user by id.

    Args:
        uid (str): User id.
        admin (User): Current user must be an admin.
        service (UsersService): Users service.

    Raises:
        AdminRightsRequired: If current user is not an admin.
        UserNotFound: If user not found.

    Returns:
        UserResponse: User object.
    """
    try:
        user = await service.get_user(uid=uid)
    except UserNotFoundError:
        raise UserNotFound()

    return UserResponse(user=UserOut(**user.dict()))


@router.post('/')
async def create_user(
    user_data: UserCreate,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[UsersService, Depends(get_users_service)],
) -> UserPasswordResponse:
    """Create user.

    Password and user id are generated automatically.
    On creation login set to user id. Can be changed later.

    See `app.core.users.generate_uid` and `app.core.security.get_password_hash`
    for more details.

    Args:
        user_data (UserCreate): User name and role.
        admin (User): Current user must be an admin.
        service (UsersService): Users service.

    Raises:
        AdminRightsRequired: If current user is not an admin.

    Returns:
        UserPasswordResponse: Created user object and generated password.
    """
    user, password = await service.create_user(
        name=user_data.name,
        role=user_data.role,
    )
    return UserPasswordResponse(
        user=UserOut(**user.dict()),
        password=password,
    )


@router.put('/{uid}')
async def update_user(
    uid: str,
    user_data: UserUpdate,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[UsersService, Depends(get_users_service)],
) -> UserResponse:
    """Update user data.

    Args:
        uid (str): User id.
        user_data (UserUpdate): User data. All fields are optional.
        admin (User): Current user must be an admin.
        service (UsersService): Users service.

    Raises:
        UserNotFound: If user not found.
        LoginAlreadyExists: If login already exists.

    Returns:
        UserResponse: Updated user object.
    """
    try:
        user = await service.update_user(
            uid=uid,
            name=user_data.name,
            login=user_data.login,
            role=user_data.role,
        )
    except UserNotFoundError:
        raise UserNotFound()
    except LoginAlreadyExistsError:
        raise LoginAlreadyExists()

    return UserResponse(user=UserOut(**user.dict()))


@router.patch('/{uid}/password')
async def update_user_password(
    uid: str,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[UsersService, Depends(get_users_service)],
) -> UserPasswordResponse:
    """Generate new password for user.

    Args:
        uid (str): User id.
        admin (User): Current user must be an admin.
        service (UsersService): Users service.

    Raises:
        AdminRightsRequired: If current user is not an admin.
        UserNotFound: If user not found.

    Returns:
        UserPasswordResponse: User object and new password.
    """
    try:
        user, password = await service.update_user_password(uid=uid)
    except UserNotFoundError:
        raise UserNotFound()

    return UserPasswordResponse(
        user=UserOut(**user.dict()),
        password=password,
    )


@router.delete('/{uid}')
async def delete_user(
    uid: str,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[UsersService, Depends(get_users_service)],
) -> UserResponse:
    """Delete user.

    Args:
        uid (str): User id.
        admin (User): Current user must be an admin.
        service (UsersService): Users service.

    Raises:
        AdminRightsRequired: If current user is not an admin.
        UserNotFound: If user not found.

    Returns:
        UserResponse: Deleted user object.
    """
    try:
        user = await service.delete_user(uid=uid)
    except UserNotFoundError:
        raise UserNotFound()

    return UserResponse(user=UserOut(**user.dict()))
