from starlette.config import Config
from starlette.datastructures import Secret
import os

class BaseConfig:

    """
    Base configuration class. Subclasses should include configurations for
    testing, development and production environments
    """
    config = Config()

    INCLUDE_SCHEMA=config("INCLUDE_SCHEMA", cast=bool, default=True)
    SERVICE_NAME = "register"

    SECRET_KEY = config("SECRET_KEY",default=os.urandom(32))
    SQLALCHEMY_ECHO = config("SQLALCHEMY_ECHO",cast=bool,default=False)
    SQLALCHEMY_TRACK_MODIFICATIONS = config("SQLALCHEMY_TRACK_MODIFICATIONS",cast=bool,default=False)

    LOGGER_NAME = "%s_log" % SERVICE_NAME
    LOG_FILENAME = "/var/tmp/app.%s.log" % SERVICE_NAME

    CORS_ORIGINS = config("CORS_HOSTS",default="*")

    DEBUG = config("DEBUG", cast=bool, default=False)
    TESTING = config("TESTING", cast=bool, default=False)


