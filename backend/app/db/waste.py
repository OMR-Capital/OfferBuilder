"""Waste model in DB."""

from typing import Any

from odetam.async_model import AsyncDetaModel
from pydantic import BaseConfig, validator

from app.models.waste import Waste


class WasteInDB(Waste, AsyncDetaModel):  # type: ignore
    """ORM model for waste."""

    class Config(BaseConfig):
        """ORM config."""

        table_name = 'wastes'

    @validator('waste_id', always=True)
    @classmethod
    def copy_id_to_key(cls, value: str, values: dict[str, Any]) -> str:
        """Copy id to key.

        Args:
            value (str): Waste id.
            values (dict[str, Any]): Waste data.

        Returns:
            str: Waste id.
        """
        values['key'] = value
        return value
