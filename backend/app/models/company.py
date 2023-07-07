"""Company model.

Companies used as an issuers of commercial offers.
"""


from pydantic import BaseModel


class Company(BaseModel):
    """Company representation in business logic."""

    # Company id
    company_id: str

    # Company name
    name: str
