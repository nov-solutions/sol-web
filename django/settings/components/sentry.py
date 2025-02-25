import logging

import sentry_sdk
import structlog
from decouple import config
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

logger = structlog.get_logger(__name__)

sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture all INFO-level logs and above
    event_level=logging.ERROR,  # Send only ERROR-level logs to Sentry
)


def configure_sentry():
    """Initialize Sentry for error tracking."""
    SENTRY_DSN = config("SENTRY_DSN", default=False)
    if not SENTRY_DSN:
        logger.warn("Sentry DSN not set, skipping Sentry setup.")
        return  # Skip setup if DSN is not set

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            sentry_logging,
        ],  # Capture logs + Django errors
        default_integrations=True,
        attach_stacktrace=True,
        send_default_pii=True,
        traces_sample_rate=1.0,
        _experiments={
            "continuous_profiling_auto_start": True,
        },
        environment=config("ENVIRONMENT"),
    )


TEST_MODE = config("TEST_MODE", "false").lower() == "true"

if not TEST_MODE:
    configure_sentry()
    logger.info("Sentry configured.")
