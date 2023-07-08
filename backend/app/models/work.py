"""Work model.

Work represents a work that company provides.
"""


from pydantic import BaseModel


class Work(BaseModel):
    """Work representation in business logic."""

    # Work id
    work_id: str

    # Work name
    name: str
