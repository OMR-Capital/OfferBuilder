"""OfferTemplate model in database."""


from typing import Any

from odetam.async_model import AsyncDetaModel
from pydantic import BaseConfig, validator

from app.models.offer_tpl import OfferTemplate


class OfferTemplateInDB(OfferTemplate, AsyncDetaModel):
    """ORM model for template."""

    class Config(BaseConfig):
        """ORM config."""

        table_name = 'offer_tpls'

    @validator('offer_tpl_id', always=True)
    @classmethod
    def copy_id_to_key(cls, value: str, values: dict[str, Any]) -> str:
        """Copy id to key.

        Args:
            value (str): Template id.
            values (dict[str, Any]): Template data.

        Returns:
            str: Template id.
        """
        values['key'] = value
        return value
