import logging
import logging.config
import sys
from logging.handlers import RotatingFileHandler

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s | %(asctime)s | %(name)s | %(message)s",
            "use_colors": True,
        },
        "verbose": {
            "format": (
                "%(levelname)s | %(asctime)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
            )
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
        "app_file": {
            "level": "DEBUG",
            "formatter": "verbose",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.log",
            "maxBytes": 5 * 1024 * 1024,  # 5 MB
            "backupCount": 3,
            "encoding": "utf8",
        },
        "uvicorn_error_file": {
            "level": "INFO",
            "formatter": "verbose",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/uvicorn_error.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 2,
            "encoding": "utf8",
        },
        "uvicorn_access_file": {
            "level": "INFO",
            "formatter": "verbose",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/uvicorn_access.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 2,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["default", "uvicorn_error_file"],
            "propagate": False,
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["default", "uvicorn_access_file"],
            "propagate": False,
        },
        "app": {
            "level": "DEBUG",
            "handlers": ["default", "app_file"],
            "propagate": False,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app")
