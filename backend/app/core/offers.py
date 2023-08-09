"""Offers utilities."""


from io import BytesIO
from typing import Any, Optional

from deta import Drive
from docxtpl import DocxTemplate

from app.core.deta import BytesIterator
from app.core.docx import (  # noqa: WPS450
    DocFormat,
    UnsupportedFileFormat,
    convert_to_pdf,
)
from app.core.models import generate_id
from app.db.offer import OfferInDB
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
        self.drive = Drive('offers')

    async def get_offers(self) -> list[Offer]:
        """Get offers.

        Returns:
            list[Offer]: Offer
        """
        db_offers = await OfferInDB.get_all()
        return [
            Offer(**db_offer.dict())
            for db_offer in db_offers
        ]

    async def get_offer(self, offer_id: str) -> Offer:
        """Get offer.

        Args:
            offer_id (str): Offer id

        Raises:
            OfferNotFoundError: If offer is not found

        Returns:
            Offer: Offer
        """
        db_offer = await OfferInDB.get_or_none(offer_id)
        if not db_offer:
            raise OfferNotFoundError()

        return Offer(**db_offer.dict())

    async def create_offer(
        self,
        name: str,
        offer_file: bytes,
    ) -> Offer:
        """Create offer.

        Args:
            name (str): Offer name
            offer_file (bytes): Offer file data

        Returns:
            Offer: Offer
        """
        offer_id = generate_id()
        await self._update_offer_file(offer_id, offer_file)

        db_offer = OfferInDB(
            offer_id=offer_id,
            name=name,
        )
        await db_offer.save()

        return Offer(**db_offer.dict())

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
        db_offer = await OfferInDB.get_or_none(offer_id)
        if not db_offer:
            raise OfferNotFoundError()

        db_offer.name = name or db_offer.name
        await db_offer.save()

        if offer_file:
            await self._update_offer_file(offer_id, offer_file)

        return Offer(**db_offer.dict())

    async def delete_offer(self, offer_id: str) -> Offer:
        """Delete offer.

        Args:
            offer_id (str): Offer id

        Raises:
            OfferNotFoundError: If offer is not found

        Returns:
            Offer: Deleted offer
        """
        db_offer = await OfferInDB.get_or_none(offer_id)
        if not db_offer:
            raise OfferNotFoundError()

        await db_offer.delete()
        self.drive.delete(offer_id)

        return Offer(**db_offer.dict())

    async def build_offer(
        self,
        name: str,
        context: dict[str, Any],
        offer_tpl_file: bytes,
    ) -> Offer:
        """Build offer file data with context.

        Args:
            name (str): Offer name
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

        offer = await self.create_offer(name, offer_file)
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
