"""Offers dependencies."""

from app.core.offers import OffersService


def get_offers_service() -> OffersService:
    """Get offers service.

    Returns:
        OffersService: Offers service.
    """
    return OffersService()
