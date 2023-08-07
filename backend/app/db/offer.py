"""Offer model in database."""


from datetime import datetime
from typing import Any

from odetam.async_model import AsyncDetaModel
from pydantic import BaseConfig, validator

from app.models.offer import Offer


class OfferInDB(Offer, AsyncDetaModel):  # type: ignore
    """ORM model for generated offer."""

    class Config(BaseConfig):
        """ORM config."""

        table_name = 'offers'

    @validator('offer_id', always=True)
    @classmethod
    def copy_id_to_key(cls, value: str, values: dict[str, Any]) -> str:
        """Copy id to key.

        Args:
            value (str): Offer id.
            values (dict[str, Any]): Offer data.

        Returns:
            str: Offer id.
        """
        values['key'] = value
        return value

    async def save(self) -> None:
        """Override save method to update modified date.

        Returns:
            _type_: _description_
        """
        self.modified_at = datetime.now()
        return await super().save()  # type: ignore
