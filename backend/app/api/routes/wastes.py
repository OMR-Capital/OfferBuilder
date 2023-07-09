"""Wastes API.

Contains CRUD operations for wastes.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_admin, get_current_user
from app.api.exceptions.wastes import WasteNotFound
from app.api.schemes.wastes import (
    WasteCreate,
    WasteListResponse,
    WasteResponse,
    WasteUpdate,
)
from app.core.models import generate_id
from app.db.waste import WasteInDB
from app.models.user import User
from app.models.waste import Waste

router = APIRouter(prefix='/wastes', tags=['wastes'])


@router.get('/')
async def get_wastes(
    user: Annotated[User, Depends(get_current_user)],
) -> WasteListResponse:
    """Get all wastes.

    Args:
        user (User): Current authorized user.

    Returns:
        WasteListResponse: List of wastes.
    """
    db_wastes = await WasteInDB.get_all()
    wastes = [Waste(**waste.dict()) for waste in db_wastes]
    return WasteListResponse(wastes=wastes)


@router.get('/{waste_id}')
async def get_waste(
    waste_id: str,
    user: Annotated[User, Depends(get_current_user)],
) -> WasteResponse:
    """Get waste by id.

    Args:
        waste_id (str): Waste id.
        user (User): Current authorized user.

    Raises:
        WasteNotFound: Raised when the waste is not found.

    Returns:
        WasteResponse: Waste.
    """
    db_waste = await WasteInDB.get_or_none(waste_id)
    if not db_waste:
        raise WasteNotFound()

    return WasteResponse(waste=Waste(**db_waste.dict()))


@router.post('/')
async def create_waste(
    waste_data: WasteCreate,
    admin: Annotated[User, Depends(get_admin)],
) -> WasteResponse:
    """Create a new waste.

    Args:
        waste_data (WasteCreate): Waste data.
        admin (User): Current user must be an admin.

    Returns:
        WasteResponse: Created waste.
    """
    waste_id = generate_id()
    db_waste = WasteInDB(
        waste_id=waste_id,
        name=waste_data.name,
        fkko_code=waste_data.fkko_code,
    )
    await db_waste.save()

    return WasteResponse(waste=Waste(**db_waste.dict()))


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
    db_waste = await WasteInDB.get_or_none(waste_id)
    if not db_waste:
        raise WasteNotFound()

    db_waste.name = waste_data.name or db_waste.name
    db_waste.fkko_code = waste_data.fkko_code or db_waste.fkko_code
    await db_waste.save()

    return WasteResponse(waste=Waste(**db_waste.dict()))


@router.delete('/{waste_id}')
async def delete_waste(
    waste_id: str,
    admin: Annotated[User, Depends(get_admin)],
) -> WasteResponse:
    """Delete waste.

    Args:
        waste_id (str): Waste id.
        admin (User): Current user must be an admin.

    Raises:
        WasteNotFound: Raised when the waste is not found.

    Returns:
        WasteResponse: Deleted waste.
    """
    db_waste = await WasteInDB.get_or_none(waste_id)
    if not db_waste:
        raise WasteNotFound()

    await db_waste.delete()
    return WasteResponse(waste=Waste(**db_waste.dict()))
