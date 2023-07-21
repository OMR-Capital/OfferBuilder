"""Waste model.

This model represent type of waste that company can recycle.
WasteItems are passed into offer table.
"""

from pydantic import BaseModel, validator

from app.core.wastes import validate_fkko_code


class Waste(BaseModel):
    """Waste representation in business logic."""

    # Waste id
    waste_id: str

    # Waste name
    name: str

    # Waste FKKO code
    fkko_code: str

    @validator('fkko_code')
    @classmethod
    def validate_fkko_code(cls, value: str) -> str:
        """Validate FKKO code.

        See `app.core.wastes.validate_fkko_code` for more information.

        P.S.
        That way used due to ODetaM limitations.

        Args:
            value (str): FKKO code.

        Raises:
            ValueError: Raised when FKKO code is invalid.

        Returns:
            str: Valid FKKO code.
        """
        if validate_fkko_code(value):
            return value

        raise ValueError('Invalid FKKO code')
