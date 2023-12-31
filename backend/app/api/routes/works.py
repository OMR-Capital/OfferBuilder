"""Works API.

Contains CRUD operations for works.
"""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_admin, get_current_user
from app.api.dependencies.works import get_works_service
from app.api.exceptions.works import WorkNotFound
from app.api.schemes.works import (
    WorkCreate,
    WorkListResponse,
    WorkResponse,
    WorkUpdate,
)
from app.core.pagination import PaginationParams
from app.core.works import WorkNotFoundError, WorksFilter, WorksService
from app.models.user import User

router = APIRouter(prefix='/works', tags=['works'])


@router.get('/')
async def get_works(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[WorksService, Depends(get_works_service)],
    pagination: Annotated[PaginationParams, Depends(PaginationParams)],
    works_filter: Annotated[Optional[WorksFilter], Depends(WorksFilter)],
) -> WorkListResponse:
    """Get all works.

    Args:
        user (User): Current authorized user.
        service (WorksService): Works service.
        pagination (PaginationParams): Pagination params.
        works_filter (WorksFilter): Works filter.

    Returns:
        WorkListResponse: List of works.
    """
    response = await service.get_works(pagination, works_filter)
    return WorkListResponse(
        works=response.items,
        last=response.last,
    )


@router.get('/{work_id}')
async def get_work(
    work_id: str,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[WorksService, Depends(get_works_service)],
) -> WorkResponse:
    """Get work by id.

    Args:
        work_id (str): Work id.
        user (User): Current authorized user.
        service (WorksService): Works service.

    Raises:
        WorkNotFound: Raised when the work is not found.

    Returns:
        WorkResponse: Work.
    """
    try:
        work = await service.get_work(work_id)
    except WorkNotFoundError:
        raise WorkNotFound()

    return WorkResponse(work=work)


@router.post('/')
async def create_work(
    work_data: WorkCreate,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[WorksService, Depends(get_works_service)],
) -> WorkResponse:
    """Create a new work.

    Args:
        work_data (WorkCreate): Work data.
        admin (User): Current user must be an admin.
        service (WorksService): Works service.

    Raises:
        BadFKKOCode: Raised when the FKKO code is invalid.

    Returns:
        WorkResponse: Created work.
    """
    work = await service.create_work(work_data.name)
    return WorkResponse(work=work)


@router.put('/{work_id}')
async def update_work(
    work_id: str,
    work_data: WorkUpdate,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[WorksService, Depends(get_works_service)],
) -> WorkResponse:
    """Update work.

    Args:
        work_id (str): Work id.
        work_data (WorkUpdate): Work data.
        admin (User): Current user must be an admin.
        service (WorksService): Works service.

    Raises:
        WorkNotFound: Raised when the work is not found.

    Returns:
        WorkResponse: Updated work.
    """
    try:
        work = await service.update_work(work_id, work_data.name)
    except WorkNotFoundError:
        raise WorkNotFound()

    return WorkResponse(work=work)


@router.delete('/{work_id}')
async def delete_work(
    work_id: str,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[WorksService, Depends(get_works_service)],
) -> WorkResponse:
    """Delete work.

    Args:
        work_id (str): Work id.
        admin (User): Current user must be an admin.
        service (WorksService): Works service.

    Raises:
        WorkNotFound: Raised when the work is not found.

    Returns:
        WorkResponse: Deleted work.
    """
    try:
        work = await service.delete_work(work_id)
    except WorkNotFoundError:
        raise WorkNotFound()

    return WorkResponse(work=work)
