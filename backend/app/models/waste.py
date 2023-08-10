"""Waste model.

This model represent type of waste that company can recycle.
WasteItems are passed into offer table.
"""

import string

from pydantic import BaseModel


class Waste(BaseModel):
    """Waste representation in business logic."""

    # Waste id
    waste_id: str

    # Waste name
    name: str

    # Waste name normalized for search
    normalized_name: str

    # Waste FKKO code
    fkko_code: str

    # Waste FKKO code normalized for search
    normalized_fkko_code: str

    @classmethod
    def normalize_name(cls, name: str) -> str:
        """Get name normalized for search.

        Remove punctuation and convert to lowercase.

        Args:
            name (str): Name.

        Returns:
            str: Normalized name.
        """
        name = name.translate(str.maketrans('', '', string.punctuation))
        return name.lower()

    @classmethod
    def normalize_fkko_code(cls, fkko_code: str) -> str:
        """Get FKKO code normalized for search.

        Remove spaces.

        Args:
            fkko_code (str): FKKO code.

        Returns:
            str: Normalized FKKO code.
        """
        return fkko_code.replace(' ', '')
