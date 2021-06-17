import os

from app.settings.settings import BaseConfig
from starlette.config import Config
from starlette.datastructures import Secret


class ProdSettings(BaseConfig):

    """Configuration class for site development environment"""

    config = Config()

    DB_USER = config("DB_USER", cast=str, default="postgres")
    DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default="postgres")
    DB_HOST = config("DB_HOST", cast=str, default="db")
    DB_PORT = config("DB_PORT", cast=str, default="5432")
    DB_NAME = config("DB_NAME", cast=str, default="postgres")
    INCLUDE_SCHEMA = config("INCLUDE_SCHEMA", cast=bool, default=False)
    SSL_CERT_FILE = config("SSL_PATH", default="/etc/.cert/ca-certificate.crt")
    ACCESS_TIMEDELTA = config("ACCESS_TIMEDELTA", cast=int, default=12)
    REFRESH_TIMEDELTA = config("REFRESH_TIMEDELTA", cast=int, default=720)  # 720
    EMAIL_TIMEDELTA = config("EMAIL_TIMEDELTA", cast=int, default=180)
    CORS_ORIGINS = config("CORS_HOSTS")
    JWT_ALGORITHM = "RS256"
    JWT_PUBLIC_KEY = open(os.getenv("JWT_PUBLIC_KEY"), "rb").read()
    JWT_PRIVATE_KEY = open(os.getenv("JWT_PRIVATE_KEY"), "rb").read()
    DATABASE_URL = config(
        "DATABASE_URL",
        default=f"asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    )
