import inspect
from functools import wraps
from logging import Logger
from typing import Any, Callable


def log_class(class_name: str, logger: Logger) -> Callable:
    def decorator(f: Callable[..., Any]) -> Callable:
        @wraps(f)
        async def logging(*args, **kwargs) -> Any:
            try:
                logger.info("ActionLog.%s.%s.start" % (class_name, f.__name__))
                if inspect.iscoroutinefunction(f):
                    tmp = await f(*args, **kwargs)
                else:
                    tmp = f(*args, **kwargs)
                logger.info("ActionLog.%s.%s.end" % (class_name, f.__name__))
                return tmp
            except Exception as e:
                logger.error(
                    "ActionLog.%s.%s.end with error %s" % (class_name, f.__name__, e)
                )
                raise e

        return logging

    return decorator


def log_function(logger: Logger) -> Callable:
    def decorator(f: Callable[..., Any]) -> Callable:
        @wraps(f)
        async def logging(*args, **kwargs) -> Any:
            try:
                logger.info("ActionLog.%s.start" % f.__name__)
                tmp = await f(*args, **kwargs)
                logger.info("ActionLog.%s.end" % f.__name__)
                return tmp
            except Exception as e:
                logger.error("ActionLog.%s.end with error %s" % (f.__name__, e))
                raise e

        return logging

    return decorator


def ClassLogger(logger: Logger):
    def aspect_log(cls):
        for attr in cls.__dict__:
            if (
                callable(getattr(cls, attr))
                and not attr.startswith("__")
                and not attr.endswith("__")
            ):
                f = log_class(cls.__name__, logger)
                setattr(cls, attr, f(getattr(cls, attr)))
        return cls

    return aspect_log
