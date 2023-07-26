"""Entry point of application.

`app` object from main module invoked by uvicorn to process requests.
"""

from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.api.routes.agents import router as agents_router
from app.api.routes.auth import router as auth_router
from app.api.routes.companies import router as companies_router
from app.api.routes.offer_tpls import router as offer_tpls_router
from app.api.routes.offers import router as offers_router
from app.api.routes.users import router as users_router
from app.api.routes.wastes import router as wastes_router
from app.api.routes.works import router as works_router


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """Simplify operation IDs.

    Used for generated API clients to have simpler function names.

    Should be called only after all routes have been added.

    See https://fastapi.tiangolo.com/ru/advanced/path-operation-advanced-configuration/ for more details. # noqa: E501

    Args:
        app (FastAPI): FastAPI application.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'


def create_app() -> FastAPI:
    """Init FastAPI application.

    Returns:
        FastAPI: FastAPI application.
    """
    app = FastAPI(
        title='Offer Builder',
        root_path='/api',
    )
    app.include_router(users_router)
    app.include_router(auth_router)
    app.include_router(companies_router)
    app.include_router(wastes_router)
    app.include_router(works_router)
    app.include_router(offers_router)
    app.include_router(offer_tpls_router)
    app.include_router(agents_router)

    return app


app = create_app()
use_route_names_as_operation_ids(app)
