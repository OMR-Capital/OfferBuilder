"""Works API.

Contains CRUD operations for works.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_admin, get_current_user
from app.api.exceptions.works import WorkNotFound
from app.api.schemes.works import (
    WorkCreate,
    WorkListResponse,
    WorkResponse,
    WorkUpdate,
)
from app.core.models import generate_id
from app.db.work import WorkInDB
from app.models.user import User
from app.models.work import Work

router = APIRouter(prefix='/works', tags=['works'])


@router.get('/')
async def get_works(
    user: Annotated[User, Depends(get_current_user)],
) -> WorkListResponse:
    """Get all works.

    Args:
        user (User): Current authorized user.

    Returns:
        WorkListResponse: List of works.
    """
    db_works = await WorkInDB.get_all()
    works = [Work(**work.dict()) for work in db_works]
    return WorkListResponse(works=works)


@router.get('/{work_id}')
async def get_work(
    work_id: str,
    user: Annotated[User, Depends(get_current_user)],
) -> WorkResponse:
    """Get work by id.

    Args:
        work_id (str): Work id.
        user (User): Current authorized user.

    Raises:
        WorkNotFound: Raised when the work is not found.

    Returns:
        WorkResponse: Work.
    """
    db_work = await WorkInDB.get_or_none(work_id)
    if not db_work:
        raise WorkNotFound()

    return WorkResponse(work=Work(**db_work.dict()))


@router.post('/')
async def create_work(
    work_data: WorkCreate,
    admin: Annotated[User, Depends(get_admin)],
) -> WorkResponse:
    """Create a new work.

    Args:
        work_data (WorkCreate): Work data.
        admin (User): Current user must be an admin.

    Returns:
        WorkResponse: Created work.
    """
    work_id = generate_id()
    work = WorkInDB(
        work_id=work_id,
        name=work_data.name,
    )
    await work.save()

    return WorkResponse(work=Work(**work.dict()))


@router.put('/{work_id}')
async def update_work(
    work_id: str,
    work_data: WorkUpdate,
    admin: Annotated[User, Depends(get_admin)],
) -> WorkResponse:
    """Update work.

    Args:
        work_id (str): Work id.
        work_data (WorkUpdate): Work data.
        admin (User): Current user must be an admin.

    Raises:
        WorkNotFound: Raised when the work is not found.

    Returns:
        WorkResponse: Updated work.
    """
    db_work = await WorkInDB.get_or_none(work_id)
    if not db_work:
        raise WorkNotFound()

    db_work.name = work_data.name
    await db_work.save()

    return WorkResponse(work=Work(**db_work.dict()))


@router.delete('/{work_id}')
async def delete_work(
    work_id: str,
    admin: Annotated[User, Depends(get_admin)],
) -> WorkResponse:
    """Delete work.

    Args:
        work_id (str): Work id.
        admin (User): Current user must be an admin.

    Raises:
        WorkNotFound: Raised when the work is not found.

    Returns:
        WorkResponse: Deleted work.
    """
    db_work = await WorkInDB.get_or_none(work_id)
    if not db_work:
        raise WorkNotFound()

    await db_work.delete()
    return WorkResponse(work=Work(**db_work.dict()))
