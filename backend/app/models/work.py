"""Work model.

Work represents a work that company provides.
"""


import re
import string

from pydantic import BaseModel


class Work(BaseModel):
    """Work representation in business logic."""

    # Work id
    work_id: str

    # Work name
    name: str

    # Work name normalized for search
    normalized_name: str

    @classmethod
    def normalize_name(cls, name: str) -> str:
        """Get name normalized for search.

        Remove punctuation and convert to lowercase.

        Args:
            name (str): Name.

        Returns:
            str: Normalized name.
        """
        name = re.sub(
            '[{punctuation}]'.format(punctuation=string.punctuation),
            ' ',
            name,
        )
        name = re.sub(r'\s+', ' ', name)
        return name.lower()
