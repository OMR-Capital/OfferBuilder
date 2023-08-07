"""Work model in database."""


from typing import Any

from odetam.async_model import AsyncDetaModel
from pydantic import BaseConfig, validator

from app.models.work import Work


class WorkInDB(Work, AsyncDetaModel):  # type: ignore
    """ORM model for work."""

    class Config(BaseConfig):
        """ORM config."""

        table_name = 'works'

    @validator('work_id', always=True)
    @classmethod
    def copy_id_to_key(cls, value: str, values: dict[str, Any]) -> str:
        """Copy id to key.

        Args:
            value (str): Work id.
            values (dict[str, Any]): Work data.

        Returns:
            str: Work id.
        """
        values['key'] = value
        return value
