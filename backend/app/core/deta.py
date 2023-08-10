"""Utilities for Deta SDK."""


import json
from io import BytesIO
from typing import Any, Iterator, Literal, Optional

from pydantic import BaseModel


def serialize_model(model: BaseModel) -> Any:
    """Serialize pydantic model to valid json.

    Args:
        model (BaseModel): Pydantic model

    Returns:
        Any: Serialized model
    """
    return json.loads(model.json())


class BytesIterator(BytesIO):
    """Wrapper for bytes iterator to IO.

    Used to wrap Drive stream body to make it readable.

    See https://docs.python.org/3/library/io.html#io.BufferedIOBase
    for more details.
    """

    def __init__(self, iterator: Iterator[bytes]) -> None:
        """Initialize wrapper.

        Args:
            iterator (Iterator[bytes]): Bytes iterator
        """
        self._iterator = iterator
        self._buffer = BytesIO()

    def read(self, size: Optional[int] = -1) -> bytes:
        """Read bytes from iterator.

        Args:
            size (int): Bytes to read. Defaults to -1.

        Returns:
            bytes: Read bytes
        """
        if size is None or size < 0:
            return b''.join(self._iterator)

        while self._buffer.tell() < size:
            try:
                self._buffer.write(next(self._iterator))
            except StopIteration:
                break

        self._buffer.seek(0)
        return self._buffer.read(size)

    def readable(self) -> Literal[True]:
        """Define that stream is readable.

        Returns:
            bool: Always True
        """
        return True

    def writable(self) -> Literal[False]:
        """Define that stream is not writable.

        Returns:
            bool: Always False
        """
        return False

    def as_iterator(self) -> Iterator[bytes]:
        """Get bytes iterator.

        Returns:
            Iterator[bytes]: Bytes iterator
        """
        return self._iterator
