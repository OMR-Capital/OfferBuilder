"""Pagination logic."""


from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Pagination params."""

    # Limit of items per page
    limit: int = Field(default=1000, ge=1, le=1000)

    # Last item id from previous page
    last: Optional[str] = None


# Can be used for default pagination value
default_pagination = PaginationParams()


ItemsType = TypeVar('ItemsType')


class PaginationResponse(BaseModel, Generic[ItemsType]):
    """Pagination response."""

    # Page items
    items: list[ItemsType]  # noqa: WPS110

    # Last item id from current page.
    # Can be used as `last` param for next page.
    # None, if there are no more pages.
    last: Optional[str] = None
