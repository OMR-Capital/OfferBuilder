"""Works business logic."""

from typing import Any, Optional

from deta import Base
from pydantic import BaseModel, validator

from app.core.deta import serialize_model
from app.core.models import generate_id
from app.core.pagination import (
    PaginationParams,
    PaginationResponse,
    default_pagination,
)
from app.models.work import Work


class WorkNotFoundError(Exception):
    """Raised when work not found."""


class WorksFilter(BaseModel):
    """Works filter."""

    name: Optional[str] = None

    name_contains: Optional[str] = None

    @validator('name', 'name_contains')
    @classmethod
    def validate_name(cls, name: Optional[str]) -> Optional[str]:
        """Validate name.

        Args:
            name (Optional[str]): Name.

        Returns:
            Optional[str]: Name if it is not None.
        """
        if name is None:
            return name

        return Work.normalize_name(name)

    def as_query(self) -> dict[str, Any]:
        """Transform filter to Deta query.

        Returns:
            dict[str, Any]: Deta query.
        """
        query = {
            'normalized_name': self.name,
            'normalized_name?contains': self.name_contains,
        }
        return {
            query: value
            for query, value in query.items()  # noqa: WPS110
            if value is not None
        }


class WorksService(object):
    """Works service.

    Provides CRUD operations for works.
    """

    def __init__(self) -> None:
        """Initialize service."""
        self.base = Base('works')

    async def get_works(
        self,
        pagination: PaginationParams = default_pagination,
        works_filter: Optional[WorksFilter] = None,
    ) -> PaginationResponse[Work]:
        """Get all works.

        Args:
            pagination (PaginationParams): Pagination params.
            works_filter (Optional[WorksFilter]): Works filter.

        Returns:
            PaginationResponse[Work]: Pagination response.
        """
        query = works_filter.as_query() if works_filter else None
        response = self.base.fetch(
            query=query,
            limit=pagination.limit,
            last=pagination.last,
        )
        works = [Work(**db_work) for db_work in response.items]
        return PaginationResponse(
            items=works,
            last=response.last,
        )

    async def get_work(self, work_id: str) -> Work:
        """Get work by id.

        Args:
            work_id (str): Work id.

        Raises:
            WorkNotFoundError: Raised when the work is not found.

        Returns:
            Work: Work object if found, None otherwise.
        """
        db_work = self.base.get(work_id)
        if db_work is None:
            raise WorkNotFoundError()

        return Work(**db_work)

    async def create_work(self, name: str) -> Work:
        """Create a new work.

        Args:
            name (str): Work name.

        Returns:
            Work: Created work.
        """
        work_id = generate_id()
        work = Work(
            work_id=work_id,
            name=name,
            normalized_name=Work.normalize_name(name),
        )
        self.base.put(serialize_model(work), work_id)
        return work

    async def update_work(
        self,
        work_id: str,
        name: Optional[str] = None,
    ) -> Work:
        """Update work.

        Args:
            work_id (str): Work id.
            name (Optional[str]): Work name.

        Raises:
            WorkNotFoundError: Raised when the work is not found.

        Returns:
            Work: Updated work.
        """
        db_work = self.base.get(work_id)
        if db_work is None:
            raise WorkNotFoundError()

        db_work['name'] = name or db_work['name']
        self.base.put(db_work, work_id)

        return Work(**db_work)

    async def delete_work(self, work_id: str) -> Work:
        """Delete work.

        Args:
            work_id (str): Work id.

        Raises:
            WorkNotFoundError: Raised when the work is not found.

        Returns:
            Work: Deleted work.
        """
        db_work = self.base.get(work_id)
        if db_work is None:
            raise WorkNotFoundError()

        self.base.delete(work_id)
        return Work(**db_work)
