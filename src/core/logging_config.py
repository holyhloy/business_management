import logging
import sys

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
        "file": {
            "level": "DEBUG",
            "formatter": "verbose",
            "class": "logging.FileHandler",
            "filename": "logs/app.log",
        },
    },
    "loggers": {
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["default", "file"],
            "propagate": False,
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["default"],
            "propagate": False,
        },
        "app": {
            "level": "DEBUG",
            "handlers": ["default", "file"],
            "propagate": False,
        },
    },
}

logger = logging.getLogger("app")
