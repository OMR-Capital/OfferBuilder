"""Works business logic."""

from typing import Optional

from app.core.models import generate_id
from app.db.work import WorkInDB
from app.models.work import Work


class WorkNotFoundError(Exception):
    """Raised when work not found."""


class WorksService(object):
    """Works service.

    Provides CRUD operations for works.
    """

    async def get_works(self) -> list[Work]:
        """Get all works.

        Returns:
            list[Work]: List of works.
        """
        db_works = await WorkInDB.get_all()
        return [Work(**work.dict()) for work in db_works]

    async def get_work(self, work_id: str) -> Work:
        """Get work by id.

        Args:
            work_id (str): Work id.

        Raises:
            WorkNotFoundError: Raised when the work is not found.

        Returns:
            Work: Work object if found, None otherwise.
        """
        db_work = await WorkInDB.get_or_none(work_id)
        if db_work is None:
            raise WorkNotFoundError()

        return Work(**db_work.dict())

    async def create_work(self, name: str) -> Work:
        """Create a new work.

        Args:
            name (str): Work name.

        Returns:
            Work: Created work.
        """
        work_id = generate_id()
        db_work = WorkInDB(
            work_id=work_id,
            name=name,
        )
        await db_work.save()
        return Work(**db_work.dict())

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
        db_work = await WorkInDB.get_or_none(work_id)
        if db_work is None:
            raise WorkNotFoundError()

        db_work.name = name or db_work.name
        await db_work.save()

        return Work(**db_work.dict())

    async def delete_work(self, work_id: str) -> Work:
        """Delete work.

        Args:
            work_id (str): Work id.

        Raises:
            WorkNotFoundError: Raised when the work is not found.

        Returns:
            Work: Deleted work.
        """
        db_work = await WorkInDB.get_or_none(work_id)
        if db_work is None:
            raise WorkNotFoundError()

        await db_work.delete()
        return Work(**db_work.dict())
