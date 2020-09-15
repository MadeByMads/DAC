from starlette.config import Config
from starlette.datastructures import Secret,URL
from core.settings.settings import BaseConfig


class DevSettings(BaseConfig):

    """ Configuration class for site development environment """

    config = Config()

    DEBUG = config("DEBUG", cast=bool, default=True)

    JWT_ALGORITHM = "RS256" 

    ACCESS_TIMEDELTA = config("DEFAULT_TIMEDELTA",cast=int,default=400)
    REFRESH_TIMEDELTA = config("DEFAULT_TIMEDELTA",cast=int,default=720)

    JWT_PUBLIC_KEY = open("/Users/tural/.cert/rsagent256.public","rb").read()
    JWT_PRIVATE_KEY = open("/Users/tural/.cert/rsagent256.private","rb").read()

    DATABASE_URL = config(
        "DATABASE_URL",
        default="asyncpg:///permissions_service",
    )   