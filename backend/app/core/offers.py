"""Offers utilities."""


from typing import Optional

from deta import Drive
# Deta has unconventional import style, so we need to use noqa here
from deta.drive import _Drive  # noqa: WPS450


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
) -> Optional[bytes]:
    """Get offer file data.

    Args:
        drive (_Drive): Offer templates drive
        offer_id (str): Offer id

    Returns:
        Optional[bytes]: Offer file data if found, None otherwise
    """
    stream = drive.get(offer_id)
    if not stream:
        return None

    # Deta is untyped, so we need to ignore type errors
    return stream.read()  # type: ignore


def save_offer_file(
    drive: _Drive,
    offer_id: str,
    offer_data: bytes,
) -> None:
    """Save offer file data.

    Args:
        drive (_Drive): Offer templates drive
        offer_id (str): Offer id
        offer_data (bytes): Offer file data
    """
    drive.put(offer_id, offer_data)


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
