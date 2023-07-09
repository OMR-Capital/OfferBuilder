"""Companies API.

Contains CRUD operations for companies.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_admin, get_current_user
from app.api.exceptions.companies import CompanyNotFound
from app.api.schemes.companies import (
    CompanyCreate,
    CompanyListResponse,
    CompanyResponse,
    CompanyUpdate,
)
from app.core.models import generate_id
from app.db.company import CompanyInDB
from app.models.company import Company
from app.models.user import User

router = APIRouter(prefix='/companies', tags=['companies'])


@router.get('/')
async def get_companies(
    user: Annotated[User, Depends(get_current_user)],
) -> CompanyListResponse:
    """Get all companies.

    Args:
        user (User): Current authorized user.

    Returns:
        CompanyListResponse: List of companies.
    """
    db_companies = await CompanyInDB.get_all()
    companies = [Company(**company.dict()) for company in db_companies]
    return CompanyListResponse(companies=companies)


@router.get('/{company_id}')
async def get_company(
    company_id: str,
    user: Annotated[User, Depends(get_current_user)],
) -> CompanyResponse:
    """Get company by id.

    Args:
        company_id (str): Company id.
        user (User): Current authorized user.

    Raises:
        CompanyNotFound: Raised when the company is not found.

    Returns:
        CompanyResponse: Company.
    """
    db_company = await CompanyInDB.get_or_none(company_id)
    if not db_company:
        raise CompanyNotFound()

    return CompanyResponse(company=Company(**db_company.dict()))


@router.post('/')
async def create_company(
    company_data: CompanyCreate,
    admin: Annotated[User, Depends(get_admin)],
) -> CompanyResponse:
    """Create a new company.

    Args:
        company_data (CompanyCreate): Company name.
        admin (User): Current user must be an admin.

    Returns:
        CompanyResponse: Created company.
    """
    company_id = generate_id()
    company = CompanyInDB(
        company_id=company_id,
        name=company_data.name,
    )
    await company.save()

    return CompanyResponse(company=Company(**company.dict()))


@router.put('/{company_id}')
async def update_company(
    company_id: str,
    company_data: CompanyUpdate,
    admin: Annotated[User, Depends(get_admin)],
) -> CompanyResponse:
    """Update company.

    Args:
        company_id (str): Company id.
        company_data (CompanyUpdate): Company name.
        admin (User): Current user must be an admin.

    Raises:
        CompanyNotFound: Raised when the company is not found.

    Returns:
        CompanyResponse: Updated company.
    """
    db_company = await CompanyInDB.get_or_none(company_id)
    if not db_company:
        raise CompanyNotFound()

    db_company.name = company_data.name
    await db_company.save()
    return CompanyResponse(company=Company(**db_company.dict()))


@router.delete('/{company_id}')
async def delete_company(
    company_id: str,
    admin: Annotated[User, Depends(get_admin)],
) -> CompanyResponse:
    """Delete company.

    Args:
        company_id (str): Company id.
        admin (User): Current user must be an admin.

    Raises:
        CompanyNotFound: Raised when the company is not found.

    Returns:
        CompanyResponse: Deleted company.
    """
    db_company = await CompanyInDB.get_or_none(company_id)
    if not db_company:
        raise CompanyNotFound()

    await db_company.delete()
    return CompanyResponse(company=Company(**db_company.dict()))
