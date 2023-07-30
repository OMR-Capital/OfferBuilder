"""MS Word docx files utilities."""


import base64
import json
from enum import Enum
from typing import Iterator, Optional

import requests

from app.api.exceptions.docx import FailConvertToPDF
from app.core.config import PDF_API_KEY


def decode_base64(file_data: str) -> Optional[bytes]:
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


class DocFormat(Enum):
    """Available document formats."""

    docx = 'docx'
    pdf = 'pdf'


PDF_API_URL_BASE = 'https://api.pspdfkit.com'


class UnsupportedFileFormat(Exception):
    """Raised when the file format is unsupported."""

    pass


def convert_to_pdf(file_data: bytes) -> Iterator[bytes]:
    """Convert docx file to PDF.

    This function actually saves the file to /temp folder
    and then converts it to PDF s:
        file_data (bytes): File data

    Raises:
        FailConvertToPDF: Raised when the file conversion failed

    Returns:
        Iterator[bytes]: Converted file data
    """
    url = '{url_base}/build'.format(url_base=PDF_API_URL_BASE)
    instructions = {
        'parts': [
            {
                'file': 'document',
            },
        ],
    }

    response = requests.post(
        url,
        files={
            'document': file_data,
        },
        headers={
            'Authorization': 'Bearer {api_key}'.format(api_key=PDF_API_KEY),
        },
        data={
            'instructions': json.dumps(instructions),
        },
        stream=True,
        timeout=10,
    )
    if not response.ok:
        raise FailConvertToPDF(response.text)

    return response.iter_content(chunk_size=1024)


def get_media_type(file_format: DocFormat) -> str:
    """Resolve MIME type for the file format.

    Args:
        file_format (DocFormat): File format

    Raises:
        UnsupportedFileFormat: Raised when the file format is unsupported

    Returns:
        str: MIME type
    """
    if file_format == DocFormat.docx:
        # flake8: noqa: E501
        return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    if file_format == DocFormat.pdf:
        return 'application/pdf'

    raise UnsupportedFileFormat()
