"""Schemes of offer templates API."""


from typing import Optional

from pydantic import BaseModel

from app.models.offer_tpl import OfferTemplate


class OfferTemplateResponse(BaseModel):
    """Offer template response scheme."""

    offer_tpl: OfferTemplate


class OfferTemplateListResponse(BaseModel):
    """Offer templates list response scheme."""

    offer_tpls: list[OfferTemplate]


class OfferTemplateCreate(BaseModel):
    """Offer template create scheme."""

    name: str
    offer_tpl_file: str


class OfferTemplateUpdate(BaseModel):
    """Offer template update scheme."""

    name: Optional[str] = None
    offer_tpl_file: Optional[str] = None
