"""Offer model."""


from datetime import datetime

from pydantic import BaseModel, Field


class Offer(BaseModel):
    """Offer representation."""

    # Offer id
    offer_id: str

    # Offer name
    name: str

    # Author name
    created_by: str

    # Create time
    created_at: datetime = Field(default_factory=datetime.now)

    # Last modification time
    modified_at: datetime = Field(default_factory=datetime.now)
