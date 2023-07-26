"""Schemes of offers API."""


from typing import Optional

from pydantic import BaseModel

from app.models.offer import Offer


class OfferResponse(BaseModel):
    """Offer response scheme."""

    offer: Offer


class OfferListResponse(BaseModel):
    """Offers list response scheme."""

    offers: list[Offer]


class OfferCreate(BaseModel):
    """Offer create scheme."""

    name: str
    offer_file: str


class OfferUpdate(BaseModel):
    """Offer update scheme."""

    name: Optional[str] = None
    offer_file: Optional[str] = None
