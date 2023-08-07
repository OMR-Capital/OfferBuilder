"""ORM company model."""


from typing import Any

from odetam.async_model import AsyncDetaModel
from pydantic import BaseConfig, validator

from app.models.company import Company


class CompanyInDB(Company, AsyncDetaModel):  # type: ignore
    """ORM model for company."""

    class Config(BaseConfig):
        """ORM config."""

        table_name = 'companies'

    @validator('company_id', always=True)
    @classmethod
    def copy_id_to_key(cls, value: str, values: dict[str, Any]) -> str:
        """Copy id to key.

        Args:
            value (str): Company id.
            values (dict[str, Any]): Company data.

        Returns:
            str: Company id.
        """
        values['key'] = value
        return value
