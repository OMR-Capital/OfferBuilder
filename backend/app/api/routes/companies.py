"""Companies API.

Contains CRUD operations for companies.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_admin, get_current_user
from app.api.dependencies.companies import get_companies_service
from app.api.exceptions.companies import CompanyNotFound
from app.api.schemes.companies import (
    CompanyCreate,
    CompanyListResponse,
    CompanyResponse,
    CompanyUpdate,
)
from app.core.companies import CompaniesService, CompanyNotFoundError
from app.models.user import User

router = APIRouter(prefix='/companies', tags=['companies'])


@router.get('/')
async def get_companies(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[CompaniesService, Depends(get_companies_service)],
) -> CompanyListResponse:
    """Get all companies.

    Args:
        user (User): Current authorized user.
        service (CompaniesService): Companies service.

    Returns:
        CompanyListResponse: List of companies.
    """
    companies = await service.get_companies()
    return CompanyListResponse(companies=companies)


@router.get('/{company_id}')
async def get_company(
    company_id: str,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[CompaniesService, Depends(get_companies_service)],
) -> CompanyResponse:
    """Get company by id.

    Args:
        company_id (str): Company id.
        user (User): Current authorized user.
        service (CompaniesService): Companies service.

    Raises:
        CompanyNotFound: Raised when the company is not found.

    Returns:
        CompanyResponse: Company.
    """
    try:
        company = await service.get_company(company_id)
    except CompanyNotFoundError:
        raise CompanyNotFound()

    return CompanyResponse(company=company)


@router.post('/')
async def create_company(
    company_data: CompanyCreate,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[CompaniesService, Depends(get_companies_service)],
) -> CompanyResponse:
    """Create a new company.

    Args:
        company_data (CompanyCreate): Company name.
        admin (User): Current user must be an admin.
        service (CompaniesService): Companies service.

    Returns:
        CompanyResponse: Created company.
    """
    company = await service.create_company(company_data.name)
    return CompanyResponse(company=company)


@router.put('/{company_id}')
async def update_company(
    company_id: str,
    company_data: CompanyUpdate,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[CompaniesService, Depends(get_companies_service)],
) -> CompanyResponse:
    """Update company.

    Args:
        company_id (str): Company id.
        company_data (CompanyUpdate): Company name.
        admin (User): Current user must be an admin.
        service (CompaniesService): Companies service.

    Raises:
        CompanyNotFound: Raised when the company is not found.

    Returns:
        CompanyResponse: Updated company.
    """
    try:
        company = await service.update_company(company_id, company_data.name)
    except CompanyNotFoundError:
        raise CompanyNotFound()

    return CompanyResponse(company=company)


@router.delete('/{company_id}')
async def delete_company(
    company_id: str,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[CompaniesService, Depends(get_companies_service)],
) -> CompanyResponse:
    """Delete company.

    Args:
        company_id (str): Company id.
        admin (User): Current user must be an admin.
        service (CompaniesService): Companies service.

    Raises:
        CompanyNotFound: Raised when the company is not found.

    Returns:
        CompanyResponse: Deleted company.
    """
    try:
        company = await service.delete_company(company_id)
    except CompanyNotFoundError:
        raise CompanyNotFound()

    return CompanyResponse(company=company)
