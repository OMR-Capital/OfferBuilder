"""Entry point of application.

`app` object from main module invoked by uvicorn to process requests.
"""

from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.companies import router as companies_router
from app.api.routes.users import router as users_router
from app.api.routes.wastes import router as wastes_router
from app.api.routes.works import router as works_router


def create_app() -> FastAPI:
    """Init FastAPI application.

    Returns:
        FastAPI: FastAPI application.
    """
    app = FastAPI(title='Offer Builder')
    app.include_router(users_router)
    app.include_router(auth_router)
    app.include_router(companies_router)
    app.include_router(wastes_router)
    app.include_router(works_router)

    return app


app = create_app()
