"""Offers templates API."""

from io import BytesIO
from typing import Annotated

# Deta has unconventional import style, so we need to use noqa here
from deta.drive import _Drive  # noqa: WPS450
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api.dependencies import get_admin, get_current_user
from app.api.exceptions.offer_tpls import (
    BadOfferTemplateFile,
    IncorrectOfferTemplateFile,
    OfferTemplateNotFound,
    OfferTemplateUploadFailed,
)
from app.api.schemes.offer_tpls import (
    OfferBuild,
    OfferTemplateCreate,
    OfferTemplateListResponse,
    OfferTemplateResponse,
    OfferTemplateUpdate,
)
from app.core.docx import decode_base64
from app.core.models import generate_id
from app.core.offer_tpls import (
    delete_offer_tpl_file,
    fill_offer_tpl,
    get_offer_tpl_file,
    get_offer_tpls_drive,
    save_offer_tpl_file,
    validate_offer_tpl_file,
)
from app.db.offer_tpl import OfferTemplateInDB
from app.models.offer_tpl import OfferTemplate
from app.models.user import User

router = APIRouter(prefix='/offer_tpls', tags=['offers templates'])


@router.get('/')
async def get_offer_tpls(
    user: Annotated[User, Depends(get_current_user)],
) -> OfferTemplateListResponse:
    """Get offer templates list.

    Args:
        user (User): Current user

    Returns:
        OfferTemplateListResponse: Offer templates list
    """
    db_offer_tpls = await OfferTemplateInDB.get_all()
    offer_tpls = [
        OfferTemplate(**offer_tpl.dict())
        for offer_tpl in db_offer_tpls
    ]
    return OfferTemplateListResponse(offer_tpls=offer_tpls)


@router.get('/{offer_tpl_id}')
async def get_offer_tpl(
    offer_tpl_id: str,
    user: Annotated[User, Depends(get_current_user)],
) -> OfferTemplateResponse:
    """Get offer template by id.

    Args:
        offer_tpl_id (str): Offer template id.
        user (User): Current user.

    Raises:
        OfferTemplateNotFound: Raised when the offer template is not found.

    Returns:
        OfferTemplateResponse: Offer template.
    """
    db_offer_tpl = await OfferTemplateInDB.get_or_none(offer_tpl_id)
    if not db_offer_tpl:
        raise OfferTemplateNotFound()

    return OfferTemplateResponse(
        offer_tpl=OfferTemplate(**db_offer_tpl.dict()),
    )


# flake8: noqa: E501
DOCX_MIME_TYPE = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'


@router.get('/{offer_tpl_id}/download')
async def download_offer_tpl(
    offer_tpl_id: str,
    drive: Annotated[_Drive, Depends(get_offer_tpls_drive)],
    user: Annotated[User, Depends(get_current_user)],
) -> StreamingResponse:
    """Download offer template file.

    Args:
        offer_tpl_id (str): Offer template id.
        drive (_Drive): Offer templates drive.
        user (User): Current user.

    Raises:
        OfferTemplateNotFound: Raised when the offer template is not found.

    Returns:
        StreamingResponse: Offer template file.
    """
    db_offer_tpl = await OfferTemplateInDB.get_or_none(offer_tpl_id)
    if not db_offer_tpl:
        raise OfferTemplateNotFound()

    offer_tpl_data = get_offer_tpl_file(drive, offer_tpl_id)
    if not offer_tpl_data:
        raise OfferTemplateNotFound()

    offer_tpl_stream = BytesIO(offer_tpl_data)
    headers = {
        'Content-Disposition': 'attachment; filename="offer.docx"',
    }
    return StreamingResponse(
        offer_tpl_stream,
        media_type=DOCX_MIME_TYPE,
        headers=headers,
    )


async def update_offer_tpl_file(
    offer_tpl_id: str,
    offer_tpl_file: str,
    drive: _Drive,
) -> None:
    """Update offer template file.

    Args:
        offer_tpl_id (str): Offer template id.
        offer_tpl_file (str): Offer template file in Base64.
        drive (_Drive): Offer templates drive.

    Raises:
        BadOfferTemplateFile: Raised when the offer template file is bad.
        IncorrectOfferTemplateFile: \
            Raised when the offer template file is incorrect.
        OfferTemplateUploadFailed: \
            Raised when the offer template upload failed.
    """
    offer_tpl_data = decode_base64(offer_tpl_file)
    if not offer_tpl_data:
        raise BadOfferTemplateFile()

    if not validate_offer_tpl_file(offer_tpl_data):
        raise IncorrectOfferTemplateFile()

    try:
        save_offer_tpl_file(drive, offer_tpl_id, offer_tpl_data)
    except Exception:
        raise OfferTemplateUploadFailed()


@router.post('/')
async def create_offer_tpl(
    offer_tpl_data: OfferTemplateCreate,
    drive: Annotated[_Drive, Depends(get_offer_tpls_drive)],
    admin: Annotated[User, Depends(get_admin)],
) -> OfferTemplateResponse:
    """Create offer template.

    Args:
        offer_tpl_data (OfferTemplateCreate): Offer template data.
        drive (_Drive): Offer templates drive.
        admin (User): Admin user.

    Returns:
        OfferTemplate: Created offer template.
    """
    offer_tpl_id = generate_id()

    await update_offer_tpl_file(
        offer_tpl_id,
        offer_tpl_data.offer_tpl_file,
        drive,
    )

    db_offer_tpl = OfferTemplateInDB(
        offer_tpl_id=offer_tpl_id,
        name=offer_tpl_data.name,
    )
    await db_offer_tpl.save()

    return OfferTemplateResponse(
        offer_tpl=OfferTemplate(**db_offer_tpl.dict()),
    )


@router.put('/{offer_tpl_id}')
async def update_offer_tpl(
    offer_tpl_id: str,
    offer_tpl_data: OfferTemplateUpdate,
    drive: Annotated[_Drive, Depends(get_offer_tpls_drive)],
    admin: Annotated[User, Depends(get_admin)],
) -> OfferTemplateResponse:
    """Update offer template.

    Args:
        offer_tpl_id (str): Offer template id.
        offer_tpl_data (OfferTemplateUpdate): Offer template data.
        drive (_Drive): Offer templates drive.
        admin (User): Admin user.

    Raises:
        OfferTemplateNotFound: Raised when the offer template is not found.

    Returns:
        OfferTemplate: Updated offer template.
    """
    db_offer_tpl = await OfferTemplateInDB.get_or_none(offer_tpl_id)
    if not db_offer_tpl:
        raise OfferTemplateNotFound()

    db_offer_tpl.name = offer_tpl_data.name or db_offer_tpl.name
    await db_offer_tpl.save()

    if offer_tpl_data.offer_tpl_file:
        await update_offer_tpl_file(
            offer_tpl_id,
            offer_tpl_data.offer_tpl_file,
            drive,
        )

    return OfferTemplateResponse(
        offer_tpl=OfferTemplate(**db_offer_tpl.dict()),
    )


@router.delete('/{offer_tpl_id}')
async def delete_offer_tpl(
    offer_tpl_id: str,
    drive: Annotated[_Drive, Depends(get_offer_tpls_drive)],
    admin: Annotated[User, Depends(get_admin)],
) -> OfferTemplateResponse:
    """Delete offer template.

    Args:
        offer_tpl_id (str): Offer template id.
        drive (_Drive): Offer templates drive.
        admin (User): Admin user.

    Raises:
        OfferTemplateNotFound: Raised when the offer template is not found.

    Returns:
        OfferTemplateResponse: Deleted offer template.
    """
    db_offer_tpl = await OfferTemplateInDB.get_or_none(offer_tpl_id)
    if not db_offer_tpl:
        raise OfferTemplateNotFound()

    await db_offer_tpl.delete()
    delete_offer_tpl_file(drive, offer_tpl_id)

    return OfferTemplateResponse(
        offer_tpl=OfferTemplate(**db_offer_tpl.dict()),
    )


@router.post('/{offer_tpl_id}/build')
async def build_offer_tpl(
    offer_tpl_id: str,
    offer_data: OfferBuild,
    drive: Annotated[_Drive, Depends(get_offer_tpls_drive)],
    user: Annotated[User, Depends(get_current_user)],
) -> StreamingResponse:
    """Fill offer template with data and return filled file.

    Args:
        offer_tpl_id (str): Offer template id.
        offer_data (OfferBuild): Offer data.
        drive (Annotated[_Drive, Depends): Offer templates drive.
        user (Annotated[User, Depends): Current user.

    Returns:
        StreamingResponse: Filled offer template file.
    """
    context = offer_data.context
    context['user'] = user

    db_offer_tpl = await OfferTemplateInDB.get_or_none(offer_tpl_id)
    if not db_offer_tpl:
        raise OfferTemplateNotFound()

    offer_tpl_data = get_offer_tpl_file(drive, offer_tpl_id)
    if not offer_tpl_data:
        raise OfferTemplateNotFound()

    filled_offer_tpl_data = fill_offer_tpl(offer_tpl_data, context)

    offer_tpl_stream = BytesIO(filled_offer_tpl_data)
    headers = {
        'Content-Disposition': 'attachment; filename="offer.docx"',
    }
    return StreamingResponse(
        offer_tpl_stream,
        media_type=DOCX_MIME_TYPE,
        headers=headers,
    )
