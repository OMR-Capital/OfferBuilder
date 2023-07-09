"""Agent model.

Agent is a target company of offers.
"""


from typing import Optional

from pydantic import BaseModel


class Agent(BaseModel):
    """Agent representation in business logic."""

    # Full company name
    fullname: str

    # Short company name
    shortname: str

    # Inn
    inn: str

    # Company principal full name. Used in offer greeting.
    # Management data can be not specified in API response.
    management: Optional[str] = None
