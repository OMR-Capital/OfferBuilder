"""Offer templates utilities."""

from io import BytesIO
from typing import Any, Optional, Union

from deta import Drive
# Deta has unconventional import style, so we need to use noqa here
from deta.drive import _Drive  # noqa: WPS450
from docxtpl.template import DocxTemplate
from jinja2.exceptions import TemplateRuntimeError

from app.api.exceptions.offer_tpls import IncorrectOfferTemplateContext
from app.core.deta import BytesIterator
from app.core.docx import DocFormat, UnsupportedFileFormat, convert_to_pdf


def get_offer_tpls_drive() -> _Drive:
    """Get offer templates drive.

    Currently, it is `offer_tpls` drive.

    Returns:
        _Drive: Offer templates drive
    """
    drive: _Drive = Drive('offer_tpls')
    return drive  # noqa: WPS331


def get_offer_tpl_file(
    drive: _Drive,
    offer_tpl_id: str,
    file_format: DocFormat,
) -> Optional[BytesIterator]:
    """Get offer template file data.

    Files stored as docx. Other formats are converted from docx.

    Args:
        drive (_Drive): Offer templates drive
        offer_tpl_id (str): Offer template id
        file_format (DocFormat): Offer template file format

    Raises:
        FailConvertToPDF: If file format is `pdf` and conversion failed
        UnsupportedFileFormat: If file format is unsupported

    Returns:
        Optional[BytesIterator]: Offer template file data if found
    """
    stream_body = drive.get(offer_tpl_id)
    if not stream_body:
        return None

    if file_format == DocFormat.docx:
        return BytesIterator(stream_body.iter_chunks())

    if file_format == DocFormat.pdf:
        file_stream = convert_to_pdf(stream_body.read())
        return BytesIterator(file_stream)

    raise UnsupportedFileFormat()


def save_offer_tpl_file(
    drive: _Drive,
    offer_tpl_id: str,
    offer_tpl_stream: Union[BytesIO, bytes],
) -> None:
    """Save offer template file data.

    Args:
        drive (_Drive): Offer templates drive
        offer_tpl_id (str): Offer template id
        offer_tpl_stream (Union[BytesIO, bytes]): Offer template file data
    """
    drive.put(offer_tpl_id, offer_tpl_stream)


def delete_offer_tpl_file(
    drive: _Drive,
    offer_tpl_id: str,
) -> None:
    """Delete offer template file data.

    Args:
        drive (_Drive): Offer templates drive
        offer_tpl_id (str): Offer template id
    """
    drive.delete(offer_tpl_id)


def validate_offer_tpl_file(
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


def fill_offer_tpl(
    offer_tpl_data: bytes,
    context: dict[str, Any],
) -> BytesIO:
    """Fill offer template file data with context.

    Args:
        offer_tpl_data (bytes): Offer template file data
        context (dict[str, Any]): Template data

    Raises:
        IncorrectOfferTemplateContext: If context is incorrect

    Returns:
        BytesIO: Filled offer template file data
    """
    offer_tpl_stream = BytesIO(offer_tpl_data)
    docx_tpl = DocxTemplate(offer_tpl_stream)
    try:
        docx_tpl.render(context)
    except TemplateRuntimeError:
        raise IncorrectOfferTemplateContext()

    filled_offer_tpl_stream = BytesIO()
    docx_tpl.save(filled_offer_tpl_stream)
    filled_offer_tpl_stream.seek(0)
    return filled_offer_tpl_stream
