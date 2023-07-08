"""Schemes of companies API."""

from pydantic import BaseModel

from app.models.company import Company


class CompanyCreate(BaseModel):
    """Create company scheme."""

    name: str


class CompanyUpdate(BaseModel):
    """Update company scheme."""

    name: str


class CompanyResponse(BaseModel):
    """Company response scheme."""

    company: Company


class CompanyListResponse(BaseModel):
    """Company list response scheme."""

    companies: list[Company]
