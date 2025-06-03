import logging
import logging.config
import sys

import structlog
from decouple import config

LOG_LEVEL = config("LOG_LEVEL", "INFO")
logging.root.setLevel(LOG_LEVEL)

# Configure Structlog to Work with Django Logs
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,  # Ensures logs are filtered by log level
        structlog.stdlib.add_logger_name,  # Adds the logger name to each log entry
        structlog.stdlib.add_log_level,  # Adds log level to structured logs
        structlog.stdlib.PositionalArgumentsFormatter(),  # Ensures args are formatted correctly
        structlog.processors.StackInfoRenderer(),  # Adds stack info to logs
        structlog.processors.format_exc_info,  # Formats exception logs properly
        structlog.processors.TimeStamper(fmt="iso"),  # Adds timestamps in ISO format
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=dict,  # Ensures context is stored as a dictionary
    logger_factory=structlog.stdlib.LoggerFactory(),  # Uses standard Python logging
    wrapper_class=structlog.stdlib.BoundLogger,  # Ensures loggers are bound correctly
    cache_logger_on_first_use=True,  # Improves performance by caching loggers
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "json_formatter",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "django": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

logging.config.dictConfig(LOGGING)
