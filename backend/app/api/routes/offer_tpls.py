"""Offers templates API."""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api.dependencies.auth import get_admin, get_current_user
from app.api.dependencies.offer_tpls import get_offer_tpls_service
from app.api.dependencies.offers import get_offers_service
from app.api.exceptions.offer_tpls import (
    BadOfferTemplateFile,
    OfferTemplateNotFound,
)
from app.api.schemes.offer_tpls import (
    BuildedOfferResponse,
    OfferBuild,
    OfferTemplateCreate,
    OfferTemplateListResponse,
    OfferTemplateResponse,
    OfferTemplateUpdate,
)
from app.core.docx import DocFormat, decode_base64, get_media_type
from app.core.offer_tpls import (
    BadOfferTemplateFileError,
    OfferTemplateNotFoundError,
    OfferTemplatesService,
)
from app.core.offers import OffersService
from app.core.pagination import PaginationParams
from app.models.user import User

router = APIRouter(prefix='/offer_tpls', tags=['offers templates'])


@router.get('/')
async def get_offer_tpls(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[OfferTemplatesService, Depends(get_offer_tpls_service)],
    pagination: Annotated[PaginationParams, Depends(PaginationParams)],
) -> OfferTemplateListResponse:
    """Get offer templates list.

    Args:
        user (User): Current user
        service (OfferTemplatesService): Offer templates service
        pagination (PaginationParams): Pagination params.

    Returns:
        OfferTemplateListResponse: Offer templates list
    """
    response = await service.get_offer_tpls(pagination)
    return OfferTemplateListResponse(
        offer_tpls=response.items,
        last=response.last,
    )


@router.get('/{offer_tpl_id}')
async def get_offer_tpl(
    offer_tpl_id: str,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[OfferTemplatesService, Depends(get_offer_tpls_service)],
) -> OfferTemplateResponse:
    """Get offer template by id.

    Args:
        offer_tpl_id (str): Offer template id.
        user (User): Current user.
        service (OfferTemplatesService): Offer templates service.

    Raises:
        OfferTemplateNotFound: Raised when the offer template is not found.

    Returns:
        OfferTemplateResponse: Offer template.
    """
    try:
        offer_tpl = await service.get_offer_tpl(offer_tpl_id)
    except OfferTemplateNotFoundError:
        raise OfferTemplateNotFound()

    return OfferTemplateResponse(offer_tpl=offer_tpl)


# flake8: noqa: E501
DOCX_MIME_TYPE = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'


@router.get('/{offer_tpl_id}/download')
async def download_offer_tpl(
    offer_tpl_id: str,
    service: Annotated[OfferTemplatesService, Depends(get_offer_tpls_service)],
    file_format: DocFormat = DocFormat.docx,
) -> StreamingResponse:
    """Download offer template file.

    Args:
        offer_tpl_id (str): Offer template id.
        output_format (DocFormat, optional): Output format. Defaults to DocFormat.docx.
        service (OfferTemplatesService): Offer templates service.

    Raises:
        OfferTemplateNotFound: Raised when the offer template is not found.
        FailConvertToPDF: Raised when the offer template conversion failed.

    Returns:
        StreamingResponse: Offer template file.
    """
    try:
        offer_tpl_stream = await service.get_offer_tpl_file(
            offer_tpl_id,
            file_format,
        )
    except OfferTemplateNotFoundError:
        raise OfferTemplateNotFound()

    return StreamingResponse(
        offer_tpl_stream.as_iterator(),
        media_type=get_media_type(file_format),
        headers={
            'Content-Disposition': 'attachment',
        },
    )


@router.post('/')
async def create_offer_tpl(
    offer_tpl_data: OfferTemplateCreate,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[OfferTemplatesService, Depends(get_offer_tpls_service)],
) -> OfferTemplateResponse:
    """Create offer template.

    Args:
        offer_tpl_data (OfferTemplateCreate): Offer template data.
        admin (User): Admin user.
        service (OfferTemplatesService): Offer templates service.

    Raises:
        BadOfferTemplateFile: Raised when the offer template file is bad.

    Returns:
        OfferTemplate: Created offer template.
    """
    offer_tpl_file_data = decode_base64(offer_tpl_data.offer_tpl_file)
    if not offer_tpl_file_data:
        raise BadOfferTemplateFile()

    try:
        offer_tpl = await service.create_offer_tpl(
            offer_tpl_data.name,
            offer_tpl_file_data,
        )
    except BadOfferTemplateFileError:
        raise BadOfferTemplateFile()

    return OfferTemplateResponse(offer_tpl=offer_tpl)


@router.put('/{offer_tpl_id}')
async def update_offer_tpl(
    offer_tpl_id: str,
    offer_tpl_data: OfferTemplateUpdate,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[OfferTemplatesService, Depends(get_offer_tpls_service)],
) -> OfferTemplateResponse:
    """Update offer template.

    Args:
        offer_tpl_id (str): Offer template id.
        offer_tpl_data (OfferTemplateUpdate): Offer template data.
        admin (User): Admin user.
        service (OfferTemplatesService): Offer templates service.

    Raises:
        OfferTemplateNotFound: Raised when the offer template is not found.

    Returns:
        OfferTemplate: Updated offer template.
    """
    if offer_tpl_data.offer_tpl_file:
        offer_tpl_file_data = decode_base64(offer_tpl_data.offer_tpl_file)
    else:
        offer_tpl_file_data = None

    try:
        offer_tpl = await service.update_offer_tpl(
            offer_tpl_id,
            offer_tpl_data.name,
            offer_tpl_file_data,
        )
    except OfferTemplateNotFoundError:
        raise OfferTemplateNotFound()

    return OfferTemplateResponse(offer_tpl=offer_tpl)


@router.delete('/{offer_tpl_id}')
async def delete_offer_tpl(
    offer_tpl_id: str,
    admin: Annotated[User, Depends(get_admin)],
    service: Annotated[OfferTemplatesService, Depends(get_offer_tpls_service)],
) -> OfferTemplateResponse:
    """Delete offer template.

    Args:
        offer_tpl_id (str): Offer template id.
        admin (User): Admin user.
        service (OfferTemplatesService): Offer templates service.

    Raises:
        OfferTemplateNotFound: Raised when the offer template is not found.

    Returns:
        OfferTemplateResponse: Deleted offer template.
    """
    try:
        offer_tpl = await service.delete_offer_tpl(offer_tpl_id)
    except OfferTemplateNotFoundError:
        raise OfferTemplateNotFound()

    return OfferTemplateResponse(offer_tpl=offer_tpl)


@router.post('/{offer_tpl_id}/build')
async def build_offer_tpl(
    offer_tpl_id: str,
    offer_data: OfferBuild,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[OfferTemplatesService, Depends(get_offer_tpls_service)],
    offers_service: Annotated[OffersService, Depends(get_offers_service)],
) -> BuildedOfferResponse:
    """Fill offer template with data and return filled file.

    Args:
        offer_tpl_id (str): Offer template id.
        offer_data (OfferBuild): Offer data.
        offers_drive (Annotated[_Drive, Depends): Offers drive.
        offer_tpls_drive (Annotated[_Drive, Depends): Offer templates drive.
        user (Annotated[User, Depends): Current user.

    Returns:
        StreamingResponse: Filled offer template file.
    """
    try:
        offer_tpl = await service.get_offer_tpl(offer_tpl_id)
        offer_tpl_stream = await service.get_offer_tpl_file(offer_tpl_id, DocFormat.docx)
    except OfferTemplateNotFoundError:
        raise OfferTemplateNotFound()

    offer_tpl_file = offer_tpl_stream.read()
    offer = await offers_service.build_offer(
        name=offer_tpl.name,
        created_by=user.name,
        context=offer_data.context,
        offer_tpl_file=offer_tpl_file,
    )

    return BuildedOfferResponse(offer=offer)
