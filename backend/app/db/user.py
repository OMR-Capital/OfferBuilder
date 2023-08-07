"""User model in DB."""

from typing import Any

from odetam.async_model import AsyncDetaModel
from pydantic import BaseConfig, validator

from app.models.user import User


class UserInDB(User, AsyncDetaModel):  # type: ignore
    """ORM model for user.

    User id is used as key.
    """

    class Config(BaseConfig):
        """ORM config."""

        table_name = 'users'

    @validator('uid', always=True)
    @classmethod
    def copy_uid_to_key(cls, value: str, values: dict[str, Any]) -> str:
        """Copy uid to key.

        Args:
            value (str): User id.
            values (dict[str, Any]): User data.

        Returns:
            str: User id.
        """
        values['key'] = value
        return value
