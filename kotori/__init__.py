import logging.config
from os import environ

# pylint: disable=C0103
is_development = environ.get("FLASK_ENV") == "development"

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)-8s] %(name)-15s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "NOTSET",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "DEBUG" if is_development else "INFO",
            "propagate": True
        }
    }
})
