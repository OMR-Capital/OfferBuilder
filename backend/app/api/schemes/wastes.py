"""Schemes of wastes API."""

from typing import Optional

from pydantic import BaseModel, validator

from app.core.wastes import validate_fkko_code
from app.models.waste import Waste


class WasteCreate(BaseModel):
    """Create waste scheme."""

    name: str
    fkko_code: str

    @validator('fkko_code')
    @classmethod
    def validate_fkko_code(cls, value: str) -> str:  # noqa: WPS110
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


class WasteUpdate(BaseModel):
    """Update waste scheme."""

    name: Optional[str]
    fkko_code: Optional[str]

    @validator('fkko_code')
    @classmethod
    def validate_fkko_code(cls, value: str) -> str:  # noqa: WPS110
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


class WasteResponse(BaseModel):
    """Waste response scheme."""

    waste: Waste


class WasteListResponse(BaseModel):
    """Waste list response scheme."""

    wastes: list[Waste]
