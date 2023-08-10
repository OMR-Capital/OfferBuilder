"""Offer templates utilities."""

from io import BytesIO
from typing import Optional

from deta import Base, Drive
from docxtpl.template import DocxTemplate

from app.core.deta import BytesIterator, serialize_model
from app.core.docx import DocFormat, UnsupportedFileFormat, convert_to_pdf
from app.core.models import generate_id
from app.core.pagination import (
    PaginationParams,
    PaginationResponse,
    default_pagination,
)
from app.models.offer_tpl import OfferTemplate


class OfferTemplateNotFoundError(Exception):
    """Offer template not found."""


class BadOfferTemplateFileError(Exception):
    """Offer template file is bad."""


class IncorrectOfferTemplateContextError(Exception):
    """Incorrect offer template context."""


class OfferTemplatesService(object):
    """Offer templates service.

    Provides methods for working with offer templates.
    """

    def __init__(self) -> None:
        """Initialize service."""
        self.base = Base('offer_tpls')
        self.drive = Drive('offer_tpls')

    async def get_offer_tpls(
        self,
        pagination: PaginationParams = default_pagination,
    ) -> PaginationResponse[OfferTemplate]:
        """Get offer templates.

        Args:
            pagination (PaginationParams): Pagination params

        Returns:
            PaginationResponse[OfferTemplate]: Pagination response
        """
        response = self.base.fetch(
            limit=pagination.limit,
            last=pagination.last,
        )
        offer_tpls = [
            OfferTemplate(**db_offer_tpl)
            for db_offer_tpl in response.items
        ]
        return PaginationResponse(
            items=offer_tpls,
            last=response.last,
        )

    async def get_offer_tpl(self, offer_tpl_id: str) -> OfferTemplate:
        """Get offer template.

        Args:
            offer_tpl_id (str): Offer template id

        Raises:
            OfferTemplateNotFoundError: If offer template is not found

        Returns:
            OfferTemplate: Offer template
        """
        db_offer_tpl = self.base.get(offer_tpl_id)
        if not db_offer_tpl:
            raise OfferTemplateNotFoundError()

        return OfferTemplate(**db_offer_tpl)

    async def create_offer_tpl(
        self,
        name: str,
        offer_tpl_file: bytes,
    ) -> OfferTemplate:
        """Create offer template.

        Args:
            name (str): Offer template name
            offer_tpl_file (bytes): Offer template file data

        Raises:
            BadOfferTemplateFileError: If offer template file is bad

        Returns:
            OfferTemplate: Offer template
        """
        offer_tpl_id = generate_id()
        await self._update_offer_tpl_file(offer_tpl_id, offer_tpl_file)

        offer_tpl = OfferTemplate(
            offer_tpl_id=offer_tpl_id,
            name=name,
        )
        self.base.put(serialize_model(offer_tpl), offer_tpl_id)

        return offer_tpl

    async def update_offer_tpl(
        self,
        offer_tpl_id: str,
        name: Optional[str] = None,
        offer_tpl_file: Optional[bytes] = None,
    ) -> OfferTemplate:
        """Update offer template.

        Args:
            offer_tpl_id (str): Offer template id
            name (Optional[str]): Offer template name
            offer_tpl_file (Optional[bytes]): Offer template file data

        Raises:
            OfferTemplateNotFoundError: If offer template is not found
            BadOfferTemplateFileError: If offer template file is bad

        Returns:
            OfferTemplate: Offer template
        """
        db_offer_tpl = self.base.get(offer_tpl_id)
        if not db_offer_tpl:
            raise OfferTemplateNotFoundError()

        db_offer_tpl['name'] = name or db_offer_tpl['name']
        self.base.put(db_offer_tpl, offer_tpl_id)

        if offer_tpl_file:
            await self._update_offer_tpl_file(offer_tpl_id, offer_tpl_file)

        return OfferTemplate(**db_offer_tpl)

    async def delete_offer_tpl(self, offer_tpl_id: str) -> OfferTemplate:
        """Delete offer template.

        Args:
            offer_tpl_id (str): Offer template id

        Raises:
            OfferTemplateNotFoundError: If offer template is not found

        Returns:
            OfferTemplate: Deleted offer template
        """
        db_offer_tpl = self.base.get(offer_tpl_id)
        if not db_offer_tpl:
            raise OfferTemplateNotFoundError()

        self.base.delete(offer_tpl_id)
        self.drive.delete(offer_tpl_id)

        return OfferTemplate(**db_offer_tpl)

    async def get_offer_tpl_file(
        self,
        offer_tpl_id: str,
        file_format: DocFormat,
    ) -> BytesIterator:
        """Get offer template file data.

        Args:
            offer_tpl_id (str): Offer template id
            file_format (DocFormat): Offer template file format

        Raises:
            OfferTemplateNotFoundError: If offer template is not found
            UnsupportedFileFormat: If file format is unsupported
            FailedToConvertToPdf: If failed to convert to pdf

        Returns:
            BytesIterator: Offer template file data
        """
        stream_body = self.drive.get(offer_tpl_id)
        if not stream_body:
            raise OfferTemplateNotFoundError()

        if file_format == DocFormat.docx:
            return BytesIterator(stream_body.iter_chunks())

        if file_format == DocFormat.pdf:
            file_stream = convert_to_pdf(stream_body.read())
            return BytesIterator(file_stream)

        raise UnsupportedFileFormat()

    async def _update_offer_tpl_file(
        self,
        offer_tpl_id: str,
        offer_tpl_data: bytes,
    ) -> None:
        """Update offer template file data.

        Args:
            offer_tpl_id (str): Offer template id
            offer_tpl_data (bytes): Offer template file data

        Raises:
            BadOfferTemplateFileError: \
                Raised when the offer template file is bad.
            IncorrectOfferTemplateFile: \
                Raised when the offer template file is incorrect.
            OfferTemplateUploadFailed: \
                Raised when the offer template upload failed.
        """
        if not self._validate_offer_tpl_file(offer_tpl_data):
            raise BadOfferTemplateFileError()

        self.drive.put(offer_tpl_id, offer_tpl_data)

    async def _validate_offer_tpl_file(
        self,
        offer_tpl_data: bytes,
    ) -> bool:
        """Validate offer template file data.

        Args:
            offer_tpl_data (bytes): Offer template file data

        Returns:
            bool: True if offer template file data is valid, False otherwise
        """
        offer_tpl_stream = BytesIO(offer_tpl_data)
        docx_tpl = DocxTemplate(offer_tpl_stream)
        try:
            docx_tpl.get_docx()
        except Exception:
            return False

        return True
