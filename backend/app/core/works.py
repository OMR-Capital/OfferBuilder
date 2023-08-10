"""Works business logic."""

from typing import Optional

from deta import Base

from app.core.deta import serialize_model
from app.core.models import generate_id
from app.models.work import Work


class WorkNotFoundError(Exception):
    """Raised when work not found."""


class WorksService(object):
    """Works service.

    Provides CRUD operations for works.
    """

    def __init__(self) -> None:
        """Initialize service."""
        self.base = Base('works')

    async def get_works(self) -> list[Work]:
        """Get all works.

        Returns:
            list[Work]: List of works.
        """
        db_works = self.base.fetch().items
        return [Work(**db_work) for db_work in db_works]

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
