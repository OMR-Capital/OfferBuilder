"""Utilities for wastes."""


import re

FKKO_CODE_PATTERN = re.compile(r'^(\d| )+$')


def validate_fkko_code(fkko_code: str) -> bool:
    """Validate FKKO code.

    FKKO code should contain only digits and spaces.
    See see http://kod-fkko.ru/ for more information.

    Args:
        fkko_code (str): FKKO code.

    Returns:
        bool: True if FKKO code is valid.
    """
    return FKKO_CODE_PATTERN.match(fkko_code) is not None
