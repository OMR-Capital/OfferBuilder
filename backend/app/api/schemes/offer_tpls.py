"""Schemes of offer templates API."""


from typing import Any, Optional

from pydantic import BaseModel

from app.models.offer import Offer
from app.models.offer_tpl import OfferTemplate


class OfferTemplateResponse(BaseModel):
    """Offer template response scheme."""

    offer_tpl: OfferTemplate


class OfferTemplateListResponse(BaseModel):
    """Offer templates list response scheme."""

    offer_tpls: list[OfferTemplate]

    last: Optional[str]


class OfferTemplateCreate(BaseModel):
    """Offer template create scheme."""

    name: str
    offer_tpl_file: str


class OfferTemplateUpdate(BaseModel):
    """Offer template update scheme."""

    name: Optional[str] = None
    offer_tpl_file: Optional[str] = None


class OfferBuild(BaseModel):
    """Offer build scheme."""

    context: dict[str, Any]


class BuildedOfferResponse(BaseModel):
    """Response scheme of builded offer."""

    offer: Offer
