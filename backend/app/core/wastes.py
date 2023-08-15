"""Utilities for wastes."""


import re
from typing import Any, Optional

from deta import Base
from pydantic import BaseModel, validator

from app.core.deta import serialize_model
from app.core.models import generate_id
from app.core.pagination import (
    PaginationParams,
    PaginationResponse,
    default_pagination,
)
from app.models.waste import Waste

FKKO_CODE_PATTERN = re.compile(r'^(\d| )+$')


class WasteNotFoundError(Exception):
    """Raised when waste not found."""


class BadFKKOCodeError(Exception):
    """Raised when FKKO code is invalid."""


class WastesFilter(BaseModel):
    """Wastes filter."""

    name: Optional[str] = None

    name_contains: Optional[str] = None

    fkko_code: Optional[str] = None

    fkko_code_prefix: Optional[str] = None

    @validator('name', 'name_contains')
    @classmethod
    def validate_name(cls, name: Optional[str]) -> Optional[str]:
        """Validate name.

        Args:
            name (Optional[str]): Name.

        Returns:
            Optional[str]: Name if it is not None.
        """
        if name is None:
            return name

        return Waste.normalize_name(name)

    @validator('fkko_code', 'fkko_code_prefix')
    @classmethod
    def validate_fkko_code(cls, fkko_code: Optional[str]) -> Optional[str]:
        """Validate FKKO code.

        Args:
            fkko_code (Optional[str]): FKKO code.

        Returns:
            Optional[str]: FKKO code if it is not None.
        """
        if fkko_code is None:
            return fkko_code

        return Waste.normalize_fkko_code(fkko_code)

    def as_query(self) -> dict[str, Any]:
        """Transform filter to Deta query.

        Returns:
            dict[str, Any]: Deta query.
        """
        query = {
            'normalized_name': self.name,
            'normalized_name?contains': self.name_contains,
            'normalized_fkko_code': self.fkko_code,
            'normalized_fkko_code?prefix': self.fkko_code_prefix,
        }
        return {
            query: value
            for query, value in query.items()  # noqa: WPS110
            if value is not None
        }


class WastesService(object):
    """Wastes service.

    Provides CRUD operations for wastes.
    """

    def __init__(self) -> None:
        """Initialize service."""
        self.base = Base('wastes')

    async def get_wastes(
        self,
        pagination: PaginationParams = default_pagination,
        wastes_filter: Optional[WastesFilter] = None,
    ) -> PaginationResponse[Waste]:
        """Get all wastes.

        Args:
            pagination (PaginationParams): Pagination params.
            wastes_filter (Optional[WastesFilter]): Wastes filter.

        Returns:
            PaginationResponse[Waste]: Pagination response.
        """
        query = wastes_filter.as_query() if wastes_filter else None
        response = self.base.fetch(
            query=query,
            limit=pagination.limit,
            last=pagination.last,
        )
        wastes = [Waste.parse_obj(db_waste) for db_waste in response.items]
        return PaginationResponse(
            items=wastes,
            last=response.last,
        )

    async def get_waste(self, waste_id: str) -> Waste:
        """Get waste by id.

        Args:
            waste_id (str): Waste id.

        Raises:
            WasteNotFoundError: Raised when the waste is not found.

        Returns:
            Waste: Waste object if found, None otherwise.
        """
        db_waste = self.base.get(waste_id)
        if db_waste is None:
            raise WasteNotFoundError()

        return Waste.parse_obj(db_waste)

    async def create_waste(
        self,
        name: str,
        fkko_code: str,
    ) -> Waste:
        """Create a new waste.

        Args:
            name (str): Waste name.
            fkko_code (str): FKKO code.

        Raises:
            BadFKKOCodeError: Raised when the FKKO code is invalid.

        Returns:
            Waste: Created waste.
        """
        if not self._validate_fkko_code(fkko_code):
            raise BadFKKOCodeError()

        waste_id = generate_id()
        waste = Waste(
            waste_id=waste_id,
            name=name,
            normalized_name=Waste.normalize_name(name),
            fkko_code=fkko_code,
            normalized_fkko_code=Waste.normalize_fkko_code(fkko_code),
        )
        self.base.put(serialize_model(waste), waste_id)

        return waste

    async def update_waste(
        self,
        waste_id: str,
        name: Optional[str] = None,
        fkko_code: Optional[str] = None,
    ) -> Waste:
        """Update waste.

        Args:
            waste_id (str): Waste id.
            name (Optional[str]): Waste name.
            fkko_code (Optional[str]): FKKO code.

        Raises:
            WasteNotFoundError: Raised when the waste is not found.
            BadFKKOCodeError: Raised when the FKKO code is invalid.

        Returns:
            Waste: Updated waste.
        """
        db_waste = self.base.get(waste_id)
        if db_waste is None:
            raise WasteNotFoundError()

        db_waste['name'] = name or db_waste['name']

        if fkko_code:
            if not self._validate_fkko_code(fkko_code):
                raise BadFKKOCodeError()

            db_waste['fkko_code'] = fkko_code

        self.base.put(db_waste, waste_id)
        return Waste.parse_obj(db_waste)

    async def delete_waste(self, waste_id: str) -> Waste:
        """Delete waste.

        Args:
            waste_id (str): Waste id.

        Raises:
            WasteNotFoundError: Raised when the waste is not found.

        Returns:
            Waste: Deleted waste.
        """
        db_waste = self.base.get(waste_id)
        if db_waste is None:
            raise WasteNotFoundError()

        self.base.delete(waste_id)

        return Waste.parse_obj(db_waste)

    def _validate_fkko_code(self, fkko_code: str) -> bool:
        """Validate FKKO code.

        FKKO code should contain only digits and spaces.
        See see http://kod-fkko.ru/ for more information.

        Args:
            fkko_code (str): FKKO code.

        Returns:
            bool: True if FKKO code is valid.
        """
        return FKKO_CODE_PATTERN.match(fkko_code) is not None
