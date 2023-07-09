"""OfferTemplate model.

Offer template is a Word document with placeholders for data from database.
See https://docxtpl.readthedocs.io/en/stable/ for more details.
"""


from pydantic import BaseModel


class OfferTemplate(BaseModel):
    """Offer template representation in business logic."""

    # Template id
    offer_tpl_id: str

    # Template name
    name: str
