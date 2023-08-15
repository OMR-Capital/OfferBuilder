"""Companies business logic."""

from deta import Base

from app.core.deta import serialize_model
from app.core.models import generate_id
from app.core.pagination import (
    PaginationParams,
    PaginationResponse,
    default_pagination,
)
from app.models.company import Company


class CompanyNotFoundError(Exception):
    """Raised when company is not found."""


class CompaniesService(object):
    """Companies service.

    Contains CRUD and manipulating operations for companies.
    """

    def __init__(self) -> None:
        """Initialize companies service."""
        self.base = Base('companies')

    async def get_companies(
        self,
        pagination: PaginationParams = default_pagination,
    ) -> PaginationResponse[Company]:
        """Get all companies.

        Args:
            pagination (PaginationParams): Pagination params.

        Returns:
            PaginationResponse[Company]: Pagination response.
        """
        response = self.base.fetch(
            limit=pagination.limit,
            last=pagination.last,
        )
        companies = [
            Company.parse_obj(db_company)
            for db_company in response.items
        ]
        return PaginationResponse(
            items=companies,
            last=response.last,
        )

    async def get_company(self, company_id: str) -> Company:
        """Get company by id.

        Args:
            company_id (str): Company id.

        Raises:
            CompanyNotFoundError: Raised when the company is not found.

        Returns:
            Company: Company instance.
        """
        db_company = self.base.get(company_id)
        if db_company is None:
            raise CompanyNotFoundError()

        return Company.parse_obj(db_company)

    async def create_company(self, name: str) -> Company:
        """Create company.

        Args:
            name (str): Company name.

        Returns:
            Company: Created company.
        """
        company_id = generate_id()
        company = Company(
            company_id=company_id,
            name=name,
        )
        self.base.put(serialize_model(company), company_id)

        return company

    async def update_company(self, company_id: str, name: str) -> Company:
        """Update company.

        Args:
            company_id (str): Company id.
            name (str): Company name.

        Raises:
            CompanyNotFoundError: Raised when the company is not found.

        Returns:
            Company: Updated company.
        """
        db_company = self.base.get(company_id)
        if db_company is None:
            raise CompanyNotFoundError()

        db_company['name'] = name
        self.base.put(db_company, company_id)

        return Company.parse_obj(db_company)

    async def delete_company(self, company_id: str) -> Company:
        """Delete company.

        Args:
            company_id (str): Company id.

        Raises:
            CompanyNotFoundError: Raised when the company is not found.

        Returns:
            Company: Deleted company.
        """
        db_company = self.base.get(company_id)
        if db_company is None:
            raise CompanyNotFoundError()

        self.base.delete(company_id)

        return Company.parse_obj(db_company)
