"""Schemes of works API."""

from typing import Optional

from pydantic import BaseModel

from app.models.work import Work


class WorkCreate(BaseModel):
    """Create work scheme."""

    name: str


class WorkUpdate(BaseModel):
    """Update work scheme."""

    name: str


class WorkResponse(BaseModel):
    """Work response scheme."""

    work: Work


class WorkListResponse(BaseModel):
    """Work list response scheme."""

    works: list[Work]

    last: Optional[str]
