"""Utilities for wastes."""


import re
from typing import Optional

from deta import Base

from app.core.deta import serialize_model
from app.core.models import generate_id
from app.models.waste import Waste

FKKO_CODE_PATTERN = re.compile(r'^(\d| )+$')


class WasteNotFoundError(Exception):
    """Raised when waste not found."""


class BadFKKOCodeError(Exception):
    """Raised when FKKO code is invalid."""


class WastesService(object):
    """Wastes service.

    Provides CRUD operations for wastes.
    """

    def __init__(self) -> None:
        """Initialize service."""
        self.base = Base('wastes')

    async def get_wastes(self) -> list[Waste]:
        """Get all wastes.

        Returns:
            list[Waste]: List of wastes.
        """
        db_wastes = self.base.fetch().items
        return [Waste(**db_waste) for db_waste in db_wastes]

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

        return Waste(**db_waste)

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
            fkko_code=fkko_code,
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
        return Waste(**db_waste)

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

        return Waste(**db_waste)

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
