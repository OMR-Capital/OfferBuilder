"""Offers utilities."""


from io import BytesIO
from typing import Any, Optional

from deta import Base, Drive
from docxtpl import DocxTemplate

from app.core.deta import BytesIterator, serialize_model
from app.core.docx import (  # noqa: WPS450
    DocFormat,
    UnsupportedFileFormat,
    convert_to_pdf,
)
from app.core.models import generate_id
from app.core.pagination import (
    PaginationParams,
    PaginationResponse,
    default_pagination,
)
from app.models.offer import Offer


class OfferNotFoundError(Exception):
    """Offer not found."""


class BadOfferFileError(Exception):
    """Offer file is bad."""


class IncorrectOfferContextError(Exception):
    """Incorrect offer context."""


class OffersService(object):
    """Offers service.

    Provides methods for working with offers.
    """

    def __init__(self) -> None:
        """Initialize service."""
        self.base = Base('offers')
        self.drive = Drive('offers')

    async def get_offers(
        self,
        pagination: PaginationParams = default_pagination,
    ) -> PaginationResponse[Offer]:
        """Get offers.

        Args:
            pagination (PaginationParams): Pagination params

        Returns:
            PaginationResponse[Offer]: Pagination response
        """
        response = self.base.fetch(
            limit=pagination.limit,
            last=pagination.last,
        )
        offers = [
            Offer.parse_obj(db_offer)
            for db_offer in response.items
        ]
        return PaginationResponse(
            items=offers,
            last=response.last,
        )

    async def get_offer(self, offer_id: str) -> Offer:
        """Get offer.

        Args:
            offer_id (str): Offer id

        Raises:
            OfferNotFoundError: If offer is not found

        Returns:
            Offer: Offer
        """
        db_offer = self.base.get(offer_id)
        if not db_offer:
            raise OfferNotFoundError()

        return Offer.parse_obj(db_offer)

    async def create_offer(
        self,
        name: str,
        created_by: str,
        offer_file: bytes,
    ) -> Offer:
        """Create offer.

        Args:
            name (str): Offer name
            created_by (str): Offer creator name
            offer_file (bytes): Offer file data

        Returns:
            Offer: Offer
        """
        offer_id = generate_id()
        await self._update_offer_file(offer_id, offer_file)

        offer = Offer(
            offer_id=offer_id,
            name=name,
            created_by=created_by,
        )
        self.base.put(serialize_model(offer), offer_id)

        return offer

    async def update_offer(
        self,
        offer_id: str,
        name: Optional[str] = None,
        offer_file: Optional[bytes] = None,
    ) -> Offer:
        """Update offer.

        Args:
            offer_id (str): Offer id
            name (Optional[str]): Offer name
            offer_file (Optional[bytes]): Offer file data

        Raises:
            OfferNotFoundError: If offer is not found

        Returns:
            Offer: Offer
        """
        db_offer = self.base.get(offer_id)
        if not db_offer:
            raise OfferNotFoundError()

        db_offer['name'] = name or db_offer['name']
        self.base.put(serialize_model(db_offer), offer_id)

        if offer_file:
            await self._update_offer_file(offer_id, offer_file)

        return Offer.parse_obj(db_offer)

    async def delete_offer(self, offer_id: str) -> Offer:
        """Delete offer.

        Args:
            offer_id (str): Offer id

        Raises:
            OfferNotFoundError: If offer is not found

        Returns:
            Offer: Deleted offer
        """
        db_offer = self.base.get(offer_id)
        if not db_offer:
            raise OfferNotFoundError()

        self.base.delete(offer_id)
        self.drive.delete(offer_id)

        return Offer.parse_obj(db_offer)

    async def build_offer(
        self,
        name: str,
        created_by: str,
        context: dict[str, Any],
        offer_tpl_file: bytes,
    ) -> Offer:
        """Build offer file data with context.

        Args:
            name (str): Offer name
            created_by (str): Offer creator name
            context (dict[str, Any]): Offer context data
            offer_tpl_file (bytes): Offer template file data

        Raises:
            OfferNotFoundError: If offer is not found
            UnsupportedFileFormat: If file format is unsupported
            FailedToConvertToPdf: If failed to convert to pdf

        Returns:
            Offer: Offer
        """
        offer_file = self._fill_offer(offer_tpl_file, context)

        offer = await self.create_offer(name, created_by, offer_file)
        await self._update_offer_file(offer.offer_id, offer_file)

        return offer

    async def get_offer_file(
        self,
        offer_id: str,
        file_format: DocFormat,
    ) -> BytesIterator:
        """Get offer file data.

        Args:
            offer_id (str): Offer id
            file_format (DocFormat): Offer file format

        Raises:
            OfferNotFoundError: If offer is not found
            UnsupportedFileFormat: If file format is unsupported
            FailedToConvertToPdf: If failed to convert to pdf

        Returns:
            BytesIterator: Offer file data
        """
        stream_body = self.drive.get(offer_id)
        if not stream_body:
            raise OfferNotFoundError()

        if file_format == DocFormat.docx:
            return BytesIterator(stream_body.iter_chunks())

        if file_format == DocFormat.pdf:
            file_stream = convert_to_pdf(stream_body.read())
            return BytesIterator(file_stream)

        raise UnsupportedFileFormat()

    async def _update_offer_file(
        self,
        offer_id: str,
        offer_data: bytes,
    ) -> None:
        """Update offer file data.

        Args:
            offer_id (str): Offer id
            offer_data (bytes): Offer file data
        """
        self.drive.put(offer_id, offer_data)

    def _fill_offer(
        self,
        offer_tpl_file: bytes,
        context: dict[str, Any],
    ) -> bytes:
        """Fill offer template with context data.

        Args:
            offer_tpl_file (bytes): Offer template file data
            context (dict[str, Any]): Offer data

        Raises:
            IncorrectOfferContextError: If context is incorrect

        Returns:
            bytes: Filled offer template file
        """
        offer_tpl_stream = BytesIO(offer_tpl_file)
        docx = DocxTemplate(offer_tpl_stream)
        try:
            docx.render(context)
        except RuntimeError:
            raise IncorrectOfferContextError()

        filled_offer_stream = BytesIO()
        docx.save(filled_offer_stream)
        filled_offer_stream.seek(0)
        return filled_offer_stream.read()
