"""Utilities for users."""

from secrets import choice
from string import ascii_letters


def generate_uid() -> str:
    """Generate user id.

    Returns:
        str: User id.
    """
    return ''.join(choice(ascii_letters) for _ in range(8))
