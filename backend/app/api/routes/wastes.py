"""Wastes API.

Contains CRUD operations for wastes.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_admin, get_current_user
from app.api.dependencies.wastes import get_wastes_service
from app.api.exceptions.wastes import BadFKKOCode, WasteNotFound
from app.api.schemes.wastes import (
    WasteCreate,
    WasteListResponse,
    WasteResponse,
    WasteUpdate,
)
from app.core.wastes import BadFKKOCodeError, WasteNotFoundError, WastesService
from app.models.user import User

router = APIRouter(prefix='/wastes', tags=['wastes'])


@router.get('/')
async def get_wastes(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[WastesService, Depends(get_wastes_service)],
) -> WasteListResponse:
    """Get all wastes.

    Args:
        user (User): Current authorized user.
        service (WastesService): Wastes service.

    Returns:
        WasteListResponse: List of wastes.
    """
    wastes = await service.get_wastes()
    return WasteListResponse(wastes=wastes)


@router.get('/{waste_id}')
async def get_waste(
    waste_id: str,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[WastesService, Depends(get_wastes_service)],
) -> WasteResponse:
    """Get waste by id.

    Args:
        waste_id (str): Waste id.
        user (User): Current authorized user.
        service (WastesService): Wastes service.

    Raises:
        WasteNotFound: Raised when the waste is not found.

    Returns:
        WasteResponse: Waste.
    """
    try:
        waste = await service.get_waste(waste_id)
    except WasteNotFoundError:
        raise WasteNotFound()

    return WasteResponse(waste=waste)


@router.post('/')
async def create_waste(
    waste_data: WasteCreate,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[WastesService, Depends(get_wastes_service)],
) -> WasteResponse:
    """Create a new waste.

    Args:
        waste_data (WasteCreate): Waste data.
        admin (User): Current user must be an admin.
        service (WastesService): Wastes service.

    Raises:
        BadFKKOCode: Raised when the FKKO code is invalid.

    Returns:
        WasteResponse: Created waste.
    """
    try:
        waste = await service.create_waste(
            name=waste_data.name,
            fkko_code=waste_data.fkko_code,
        )
    except BadFKKOCodeError:
        raise BadFKKOCode()

    return WasteResponse(waste=waste)


@router.put('/{waste_id}')
async def update_waste(
    waste_id: str,
    waste_data: WasteUpdate,
    admin: Annotated[User, Depends(get_admin)],
) -> WasteResponse:
    """Update waste.

    Args:
        waste_id (str): Waste id.
        waste_data (WasteUpdate): Waste data.
        admin (User): Current user must be an admin.

    Raises:
        WasteNotFound: Raised when the waste is not found.

    Returns:
        WasteResponse: Updated waste.
    """
    try:
        waste = await WastesService().update_waste(
            waste_id=waste_id,
            name=waste_data.name,
            fkko_code=waste_data.fkko_code,
        )
    except WasteNotFoundError:
        raise WasteNotFound()

    return WasteResponse(waste=waste)


@router.delete('/{waste_id}')
async def delete_waste(
    waste_id: str,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[WastesService, Depends(get_wastes_service)],
) -> WasteResponse:
    """Delete waste.

    Args:
        waste_id (str): Waste id.
        admin (User): Current user must be an admin.
        service (WastesService): Wastes service.

    Raises:
        WasteNotFound: Raised when the waste is not found.

    Returns:
        WasteResponse: Deleted waste.
    """
    try:
        waste = await service.delete_waste(waste_id)
    except WasteNotFoundError:
        raise WasteNotFound()

    return WasteResponse(waste=waste)
