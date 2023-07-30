"""Offers API."""


from typing import Annotated

# Deta has unconventional import style, so we need to use noqa here
from deta.drive import _Drive  # noqa: WPS450
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api.dependencies import get_admin, get_current_user
from app.api.exceptions.offers import (
    BadOfferFile,
    OfferNotFound,
    OfferUploadFailed,
)
from app.api.schemes.offers import (
    OfferCreate,
    OfferListResponse,
    OfferResponse,
    OfferUpdate,
)
from app.core.docx import DocFormat, decode_base64, get_media_type
from app.core.models import generate_id
from app.core.offers import (
    delete_offer_file,
    get_offer_file,
    get_offers_drive,
    save_offer_file,
)
from app.db.offer import OfferInDB
from app.models.offer import Offer
from app.models.user import User

router = APIRouter(prefix='/offers', tags=['offers'])


@router.get('/')
async def get_offers(
    user: Annotated[User, Depends(get_current_user)],
) -> OfferListResponse:
    """Get offers list.

    Args:
        user (User): Current user

    Returns:
        OfferListResponse: Offers list
    """
    db_offers = await OfferInDB.get_all()
    offers = [
        Offer(**offer.dict())
        for offer in db_offers
    ]
    return OfferListResponse(offers=offers)


@router.get('/{offer_id}')
async def get_offer(
    offer_id: str,
    user: Annotated[User, Depends(get_current_user)],
) -> OfferResponse:
    """Get offer by id.

    Args:
        offer_id (str): Offer id.
        user (User): Current user.

    Raises:
        OfferNotFound: Raised when the offer is not found.

    Returns:
        OfferResponse: Offer.
    """
    db_offer = await OfferInDB.get_or_none(offer_id)
    if not db_offer:
        raise OfferNotFound()

    return OfferResponse(
        offer=Offer(**db_offer.dict()),
    )


@router.get('/{offer_id}/download')
async def download_offer(
    offer_id: str,
    drive: Annotated[_Drive, Depends(get_offers_drive)],
    file_format: DocFormat = DocFormat.docx,
) -> StreamingResponse:
    """Download offer file.

    Args:
        offer_id (str): Offer id.
        drive (_Drive): Offers drive.
        file_format (DocFormat): Output format. Defaults to DocFormat.docx.

    Raises:
        OfferNotFound: Raised when the offer is not found.
        FailConvertToPDF: Raised when the offer file is bad.

    Returns:
        StreamingResponse: Offer file.
    """
    db_offer = await OfferInDB.get_or_none(offer_id)
    if not db_offer:
        raise OfferNotFound()

    offer_stream = get_offer_file(drive, offer_id, file_format)
    if not offer_stream:
        raise OfferNotFound()

    return StreamingResponse(
        offer_stream.as_iterator(),
        media_type=get_media_type(file_format),
        headers={
            'Content-Disposition': 'attachment',
        },
    )


async def update_offer_file(
    offer_id: str,
    offer_file: str,
    drive: _Drive,
) -> None:
    """Update offer file.

    Args:
        offer_id (str): Offer id.
        offer_file (str): Offer file in Base64.
        drive (_Drive): Offers drive.

    Raises:
        BadOfferFile: Raised when the offer file is bad.
        IncorrectOfferFile: \
            Raised when the offer file is incorrect.
        OfferUploadFailed: \
            Raised when the offer upload failed.
    """
    offer_stream = decode_base64(offer_file)
    if not offer_stream:
        raise BadOfferFile()

    try:
        save_offer_file(drive, offer_id, offer_stream)
    except Exception:
        raise OfferUploadFailed()


@router.post('/')
async def create_offer(
    offer_data: OfferCreate,
    drive: Annotated[_Drive, Depends(get_offers_drive)],
    admin: Annotated[User, Depends(get_admin)],
) -> OfferResponse:
    """Create offer.

    Args:
        offer_data (OfferCreate): Offer data.
        drive (_Drive): Offers drive.
        admin (User): Admin user.

    Returns:
        OfferResponse: Created offer.
    """
    offer_id = generate_id()

    await update_offer_file(
        offer_id,
        offer_data.offer_file,
        drive,
    )

    db_offer = OfferInDB(
        offer_id=offer_id,
        name=offer_data.name,
    )
    await db_offer.save()

    return OfferResponse(
        offer=Offer(**db_offer.dict()),
    )


@router.put('/{offer_id}')
async def update_offer(
    offer_id: str,
    offer_data: OfferUpdate,
    drive: Annotated[_Drive, Depends(get_offers_drive)],
    admin: Annotated[User, Depends(get_admin)],
) -> OfferResponse:
    """Update offer.

    Args:
        offer_id (str): Offer id.
        offer_data (OfferUpdate): Offer data.
        drive (_Drive): Offers drive.
        admin (User): Admin user.

    Raises:
        OfferNotFound: Raised when the offer is not found.

    Returns:
        OfferResponse: Updated offer.
    """
    db_offer = await OfferInDB.get_or_none(offer_id)
    if not db_offer:
        raise OfferNotFound()

    db_offer.name = offer_data.name or db_offer.name
    await db_offer.save()

    if offer_data.offer_file:
        await update_offer_file(
            offer_id,
            offer_data.offer_file,
            drive,
        )

    return OfferResponse(
        offer=Offer(**db_offer.dict()),
    )


@router.delete('/{offer_id}')
async def delete_offer(
    offer_id: str,
    drive: Annotated[_Drive, Depends(get_offers_drive)],
    admin: Annotated[User, Depends(get_admin)],
) -> OfferResponse:
    """Delete offer.

    Args:
        offer_id (str): Offer id.
        drive (_Drive): Offers drive.
        admin (User): Admin user.

    Raises:
        OfferNotFound: Raised when the offer is not found.

    Returns:
        OfferResponse: Deleted offer.
    """
    db_offer = await OfferInDB.get_or_none(offer_id)
    if not db_offer:
        raise OfferNotFound()

    await db_offer.delete()
    delete_offer_file(drive, offer_id)

    return OfferResponse(
        offer=Offer(**db_offer.dict()),
    )
