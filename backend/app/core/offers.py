"""Offers utilities."""


from io import BytesIO
from typing import Optional, Union

from deta import Drive
# Deta has unconventional import style, so we need to use noqa here
from deta.drive import _Drive  # noqa: WPS450

from app.core.deta import BytesIterator
from app.core.docx import (  # noqa: WPS450
    DocFormat,
    UnsupportedFileFormat,
    convert_to_pdf,
)


def get_offers_drive() -> _Drive:
    """Get offer templates drive.

    Currently, it is `offer_tpls` drive.

    Returns:
        _Drive: Offer templates drive
    """
    # Deta is untyped, so we need to ignore type errors
    return Drive('offers')  # type: ignore


def get_offer_file(
    drive: _Drive,
    offer_id: str,
    file_format: DocFormat,
) -> Optional[BytesIterator]:
    """Get offer file data.

    Args:
        drive (_Drive): Offer templates drive
        offer_id (str): Offer id
        file_format (DocFormat): Offer file format

    Raises:
        FailConvertToPDF: If file format is `pdf` and conversion failed
        UnsupportedFileFormat: If file format is unsupported

    Returns:
        Optional[DocFormat]: Offer file data if found
    """
    stream_body = drive.get(offer_id)
    if not stream_body:
        return None

    if file_format == DocFormat.docx:
        return BytesIterator(stream_body.iter_chunks())

    if file_format == DocFormat.pdf:
        file_stream = convert_to_pdf(stream_body.read())
        return BytesIterator(file_stream)

    raise UnsupportedFileFormat()


def save_offer_file(
    drive: _Drive,
    offer_id: str,
    offer_stream: Union[BytesIO, bytes],
) -> None:
    """Save offer file data.

    Args:
        drive (_Drive): Offer templates drive
        offer_id (str): Offer id
        offer_stream (Union[BytesIO, bytes]): Offer file data
    """
    drive.put(offer_id, offer_stream)


def delete_offer_file(
    drive: _Drive,
    offer_id: str,
) -> None:
    """Delete offer file data.

    Args:
        drive (_Drive): Offer templates drive
        offer_id (str): Offer id
    """
    drive.delete(offer_id)
