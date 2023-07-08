"""Schemes of wastes API."""

from pydantic import BaseModel

from app.models.waste import FKKOCode, Waste


class WasteCreate(BaseModel):
    """Create waste scheme."""

    name: str
    fkko_code: FKKOCode


class WasteUpdate(BaseModel):
    """Update waste scheme."""

    name: str
    fkko_code: FKKOCode


class WasteResponse(BaseModel):
    """Waste response scheme."""

    waste: Waste


class WasteListResponse(BaseModel):
    """Waste list response scheme."""

    wastes: list[Waste]
