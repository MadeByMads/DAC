import logging
from ssl import create_default_context

import coloredlogs
from gino.ext.starlette import Gino

from core.factories import settings

if not settings.DEBUG:
    ssl_object = create_default_context(cafile=settings.SSL_CERT_FILE)

    db: Gino = Gino(
        dsn=settings.DATABASE_URL,
        ssl=ssl_object,
        pool_min_size=3,
        pool_max_size=20,
        retry_limit=1,
        retry_interval=1,
    )
else:

    db: Gino = Gino(dsn=settings.DATABASE_URL, echo=False)


# def get_logger(log_level="DEBUG"):
#     if not settings.DEBUG:
#         logger = logging.getLogger("gunicorn.error")
#     else:
#         logger = logging.getLogger()

#     colors_config = coloredlogs.DEFAULT_LEVEL_STYLES
#     coloredlogs.DEFAULT_LOG_FORMAT = (
#         "%(asctime)s %(hostname)s %(name)s %(levelname)s %(message)s"
#     )
#     colors_config.update(**{"info": {"color": "white", "faint": True}})
#     logger.setLevel(log_level)
#     coloredlogs.install(level=log_level, logger=logger)

#     return logger


# log = get_logger()
