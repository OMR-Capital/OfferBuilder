"""Entry point of application.

`app` object from main module invoked by uvicorn to process requests.
"""

from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router


def create_app() -> FastAPI:
    """Init FastAPI application.

    Returns:
        FastAPI: FastAPI application.
    """
    app = FastAPI(title='Offer Builder')
    app.include_router(users_router)
    app.include_router(auth_router)

    return app


app = create_app()
