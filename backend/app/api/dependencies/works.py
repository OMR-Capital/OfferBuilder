"""Works dependencies."""


from app.core.works import WorksService


def get_works_service() -> WorksService:
    """Get works service.

    Returns:
        WorksService: Works service.
    """
    return WorksService()
