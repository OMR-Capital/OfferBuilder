"""Waste model.

This model represent type of waste that company can recycle.
WasteItems are passed into offer table.
"""

from pydantic import BaseModel


class Waste(BaseModel):
    """Waste representation in business logic."""

    # Waste id
    waste_id: str

    # Waste name
    name: str

    # Waste FKKO code
    fkko_code: str
