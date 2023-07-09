"""Schemes of wastes API."""

from typing import Optional

from pydantic import BaseModel

from app.models.waste import FKKOCode, Waste


class WasteCreate(BaseModel):
    """Create waste scheme."""

    name: str
    fkko_code: FKKOCode


class WasteUpdate(BaseModel):
    """Update waste scheme."""

    name: Optional[str]
    fkko_code: Optional[FKKOCode]


class WasteResponse(BaseModel):
    """Waste response scheme."""

    waste: Waste


class WasteListResponse(BaseModel):
    """Waste list response scheme."""

    wastes: list[Waste]
