"""Offers API."""


from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api.dependencies.auth import get_admin, get_current_user
from app.api.dependencies.offers import get_offers_service
from app.api.exceptions.offers import BadOfferFile, OfferNotFound
from app.api.schemes.offers import (
    OfferCreate,
    OfferListResponse,
    OfferResponse,
    OfferUpdate,
)
from app.core.docx import DocFormat, decode_base64, get_media_type
from app.core.offers import OfferNotFoundError, OffersService
from app.core.pagination import PaginationParams
from app.models.user import User

router = APIRouter(prefix='/offers', tags=['offers'])


@router.get('/')
async def get_offers(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[OffersService, Depends(get_offers_service)],
    pagination: Annotated[PaginationParams, Depends(PaginationParams)],
) -> OfferListResponse:
    """Get offers list.

    Args:
        user (User): Current user
        service (OffersService): Offers service
        pagination (PaginationParams): Pagination params.

    Returns:
        OfferListResponse: Offers list
    """
    response = await service.get_offers(pagination)
    return OfferListResponse(
        offers=response.items,
        last=response.last,
    )


@router.get('/{offer_id}')
async def get_offer(
    offer_id: str,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[OffersService, Depends(get_offers_service)],
) -> OfferResponse:
    """Get offer by id.

    Args:
        offer_id (str): Offer id.
        user (User): Current user.
        service (OffersService): Offers service.

    Raises:
        OfferNotFound: Raised when the offer is not found.

    Returns:
        OfferResponse: Offer.
    """
    try:
        offer = await service.get_offer(offer_id)
    except OfferNotFoundError:
        raise OfferNotFound()

    return OfferResponse(offer=offer)


@router.get('/{offer_id}/download')
async def download_offer(
    offer_id: str,
    service: Annotated[OffersService, Depends(get_offers_service)],
    file_format: DocFormat = DocFormat.docx,
) -> StreamingResponse:
    """Download offer file.

    Args:
        offer_id (str): Offer id.
        file_format (DocFormat): Output format. Defaults to DocFormat.docx.
        service (OffersService): Offers service.

    Raises:
        OfferNotFound: Raised when the offer is not found.
        FailConvertToPDF: Raised when the offer file is bad.

    Returns:
        StreamingResponse: Offer file.
    """
    try:
        offer_stream = await service.get_offer_file(offer_id, file_format)
    except OfferNotFoundError:
        raise OfferNotFound()

    return StreamingResponse(
        offer_stream.as_iterator(),
        media_type=get_media_type(file_format),
        headers={
            'Content-Disposition': 'attachment',
        },
    )


@router.post('/')
async def create_offer(
    offer_data: OfferCreate,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[OffersService, Depends(get_offers_service)],
) -> OfferResponse:
    """Create offer.

    Args:
        offer_data (OfferCreate): Offer data.
        admin (User): Admin user.
        service (OffersService): Offers service.

    Raises:
        BadOfferFile: Raised when the offer file is bad.

    Returns:
        OfferResponse: Created offer.
    """
    offer_file = decode_base64(offer_data.offer_file)
    if not offer_file:
        raise BadOfferFile()

    offer = await service.create_offer(
        name=offer_data.name,
        created_by=admin.name,
        offer_file=offer_file,
    )
    return OfferResponse(offer=offer)


@router.put('/{offer_id}')
async def update_offer(
    offer_id: str,
    offer_data: OfferUpdate,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[OffersService, Depends(get_offers_service)],
) -> OfferResponse:
    """Update offer.

    Args:
        offer_id (str): Offer id.
        offer_data (OfferUpdate): Offer data.
        admin (User): Admin user.
        service (OffersService): Offers service.

    Raises:
        OfferNotFound: Raised when the offer is not found.

    Returns:
        OfferResponse: Updated offer.
    """
    try:
        offer = await service.update_offer(
            offer_id,
            name=offer_data.name,
        )
    except OfferNotFoundError:
        raise OfferNotFound()

    return OfferResponse(offer=offer)


@router.delete('/{offer_id}')
async def delete_offer(
    offer_id: str,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[OffersService, Depends(get_offers_service)],
) -> OfferResponse:
    """Delete offer.

    Args:
        offer_id (str): Offer id.
        admin (User): Admin user.
        service (OffersService): Offers service.

    Raises:
        OfferNotFound: Raised when the offer is not found.

    Returns:
        OfferResponse: Deleted offer.
    """
    try:
        offer = await service.delete_offer(offer_id)
    except OfferNotFoundError:
        raise OfferNotFound()

    return OfferResponse(offer=offer)
