"""Users dependencies."""

from app.core.users import UsersService


def get_users_service() -> UsersService:
    """Get users service.

    Returns:
        UsersService: Users service.
    """
    return UsersService()
