from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import settings
from app.api import api_router


def init_app(app: FastAPI):
    """
    Initialise routers and database.
    """
    init_routers(app)
    init_db(app)


def init_db(app: FastAPI):
    """
    Initialise database models.
    """
    register_tortoise(
        app,
        db_url=settings.DB_URL,
        modules={"models": settings.DB_MODELS},
        generate_schemas=True
    )


def init_routers(app: FastAPI):
    """
    Initialise routers in `app.api.routers`
    """
    app.include_router(
        api_router
    )
