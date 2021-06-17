import os

from starlette.config import Config
from starlette.datastructures import Secret


class BaseConfig:

    """
    Base configuration class. Subclasses should include configurations for
    testing, development and production environments
    """

    config = Config()

    INCLUDE_SCHEMA = config("INCLUDE_SCHEMA", cast=bool, default=True)
    SERVICE_NAME = "DAC-service"

    SECRET_KEY = config("SECRET_KEY", default=os.urandom(32))
    SQLALCHEMY_ECHO = config("SQLALCHEMY_ECHO", cast=bool, default=False)
    SQLALCHEMY_TRACK_MODIFICATIONS = config(
        "SQLALCHEMY_TRACK_MODIFICATIONS", cast=bool, default=False
    )

    LOGGER_NAME = "%s_log" % SERVICE_NAME
    LOG_FILENAME = "/var/tmp/app.%s.log" % SERVICE_NAME
    JWT_PUBLIC_KEY = open("/Users/tmuradov/.cert/publickey.crt", "rb").read()
    JWT_PRIVATE_KEY = open("/Users/tmuradov/.cert/pkcs8.key", "rb").read()
    CORS_ORIGINS = config("CORS_HOSTS", default="*")
    JWT_ALGORITHM = "RS256"
    JWT_ISSUER = config("JWT_ISSUER", cast=str, default="DAC-PROJECT")
    JWT_ACCESS_TIMEDELTA = config("DEFAULT_TIMEDELTA", cast=int, default=720)
    JWT_REFRESH_TIMEDELTA = config("DEFAULT_TIMEDELTA", cast=int, default=720)  # 720
    JWT_EMAIL_TIMEDELTA = config("EMAIL_TIMEDELTA", cast=int, default=1)
    DEBUG = config("DEBUG", cast=bool, default=False)
    TESTING = config("TESTING", cast=bool, default=False)
