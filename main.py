from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import settings
from app.core import init_app


# Initialise FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION
)

# Connect database and routers
init_app(app)

