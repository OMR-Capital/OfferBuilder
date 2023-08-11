"""Wastes dependencies."""


from app.core.wastes import WastesService


def get_wastes_service() -> WastesService:
    """Get wastes service.

    Returns:
        WastesService: Wastes service.
    """
    return WastesService()
