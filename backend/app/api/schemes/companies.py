"""Schemes of companies API."""

from pydantic import BaseModel

from app.models.company import Company


class CompanyResponse(BaseModel):
    """User response scheme."""

    company: Company


class CompanyListResponse(BaseModel):
    """User list response scheme."""

    companies: list[Company]
