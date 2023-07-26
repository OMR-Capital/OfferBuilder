"""MS Word docx files utilities."""


import base64
from typing import Optional


def decode_base64(
    file_data: str,
) -> Optional[bytes]:
    """Decode docx file from base64.

    Args:
        file_data (str): File data in Base64

    Returns:
        Optional[bytes]: Decoded file
    """
    try:
        return base64.b64decode(file_data)
    except Exception:
        return None
