from app.settings.settings import BaseConfig
from starlette.config import Config
from starlette.datastructures import Secret


class DevSettings(BaseConfig):

    """Configuration class for site development environment"""

    config = Config()

    DEBUG = config("DEBUG", cast=bool, default=True)

    DB_USER = config("DB_USER", cast=str, default="postgres")
    DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default="postgres")
    DB_HOST = config("DB_HOST", cast=str, default="db")
    DB_PORT = config("DB_PORT", cast=str, default="5432")
    DB_NAME = config("DB_NAME", cast=str, default="postgres")
    INCLUDE_SCHEMA = config("INCLUDE_SCHEMA", cast=bool, default=True)
    DAC_URL = "http://127.0.0.1:8000"

    DATABASE_URL = config(
        "DATABASE_URL",
        default=f"asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    )
