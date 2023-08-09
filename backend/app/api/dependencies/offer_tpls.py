"""Offer templates dependencies."""

from app.core.offer_tpls import OfferTemplatesService


def get_offer_tpls_service() -> OfferTemplatesService:
    """Get offer templates service.

    Returns:
        OfferTemplatesService: Offer templates service.
    """
    return OfferTemplatesService()
