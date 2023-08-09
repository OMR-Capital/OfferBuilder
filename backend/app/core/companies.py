"""Companies business logic."""


from app.core.models import generate_id
from app.db.company import CompanyInDB
from app.models.company import Company


class CompanyNotFoundError(Exception):
    """Raised when company is not found."""


class CompaniesService(object):
    """Companies service.

    Contains CRUD and manipulating operations for companies.
    """

    async def get_companies(self) -> list[Company]:
        """Get all companies.

        Returns:
            List[Company]: List of companies.
        """
        db_companies = await CompanyInDB.get_all()
        return [Company(**company.dict()) for company in db_companies]

    async def get_company(self, company_id: str) -> Company:
        """Get company by id.

        Args:
            company_id (str): Company id.

        Raises:
            CompanyNotFoundError: Raised when the company is not found.

        Returns:
            Company: Company instance.
        """
        db_company = await CompanyInDB.get(company_id)
        if db_company is None:
            raise CompanyNotFoundError()

        return Company(**db_company.dict())

    async def create_company(self, name: str) -> Company:
        """Create company.

        Args:
            name (str): Company name.

        Returns:
            Company: Created company.
        """
        company_id = generate_id()
        company = CompanyInDB(
            company_id=company_id,
            name=name,
        )
        await company.save()

        return Company(**company.dict())

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
        db_company = await CompanyInDB.get_or_none(company_id)
        if db_company is None:
            raise CompanyNotFoundError()

        db_company.name = name
        await db_company.save()

        return Company(**db_company.dict())

    async def delete_company(self, company_id: str) -> Company:
        """Delete company.

        Args:
            company_id (str): Company id.

        Raises:
            CompanyNotFoundError: Raised when the company is not found.

        Returns:
            Company: Deleted company.
        """
        db_company = await CompanyInDB.get_or_none(company_id)
        if db_company is None:
            raise CompanyNotFoundError()

        await db_company.delete()

        return Company(**db_company.dict())
