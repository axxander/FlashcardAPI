from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    All application settings stored in Settings object.
    """

    # encryption settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 30

    # tortoise ORM settings
    DB_MODELS: List[str] = ["app.models"]
    DB_URL: str = "sqlite://flashapp.db"

    # openapi settings
    API_TITLE: str = "Flashcards"
    API_VERSION: str = "0.0.1 beta"
    API_DESCRIPTION: str = "CRUD RESTfulAPI for flashcards"


    class Config:
        env_file = "app/core/.env"
        env_file_encoding = "utf-8"
        case_sensitive=True


settings = Settings()
