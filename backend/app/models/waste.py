"""Waste model.

This model represent type of waste that company can recycle.
WasteItems are passed into offer table.
"""


from pydantic import BaseModel, ConstrainedStr


class FKKOCode(ConstrainedStr):
    """FKKO code representation.

    See see http://kod-fkko.ru/ for more information.
    """

    min_length = 1
    regex = r'(\d| )+'


class Waste(BaseModel):
    """Waste representation in business logic."""

    # Waste id
    waste_id: str

    # Waste name
    name: str

    # Waste FKKO code
    fkko_code: FKKOCode
