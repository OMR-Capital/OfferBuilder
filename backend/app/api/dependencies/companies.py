"""Companies dependencies."""

from app.core.companies import CompaniesService


def get_companies_service() -> CompaniesService:
    """Get companies service.

    Returns:
        CompaniesService: Companies service.
    """
    return CompaniesService()
