"""Utilities for models."""


from secrets import choice
from string import ascii_letters, digits

ID_ALPHABET = ascii_letters + digits
ID_SIZE = 12


def generate_id() -> str:
    """Generate random 12-symbols id.

    Returns:
        str: Id.
    """
    return ''.join(choice(ID_ALPHABET) for _ in range(ID_SIZE))
