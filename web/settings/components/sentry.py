import logging
import os
from urllib.parse import urlparse

import sentry_sdk
import structlog
from decouple import config
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

logger = structlog.get_logger(__name__)

# Sentry Configuration
SENTRY_DSN = config("SENTRY_DSN", default="")
SENTRY_ENVIRONMENT = config(
    "SENTRY_ENVIRONMENT", default=config("ENVIRONMENT", "development")
)
SENTRY_RELEASE = config("SENTRY_RELEASE", default=os.environ.get("GIT_SHA", "unknown"))
SENTRY_TRACES_SAMPLE_RATE = config("SENTRY_TRACES_SAMPLE_RATE", default=0.1, cast=float)
SENTRY_PROFILES_SAMPLE_RATE = config(
    "SENTRY_PROFILES_SAMPLE_RATE", default=0.1, cast=float
)
SENTRY_SEND_DEFAULT_PII = config("SENTRY_SEND_DEFAULT_PII", default=False, cast=bool)
SENTRY_DEBUG = config("SENTRY_DEBUG", default=False, cast=bool)
SENTRY_ATTACH_STACKTRACE = config("SENTRY_ATTACH_STACKTRACE", default=True, cast=bool)
SENTRY_REQUEST_BODIES = config(
    "SENTRY_REQUEST_BODIES", default="medium"
)  # never, small, medium, always
SENTRY_WITH_LOCALS = config("SENTRY_WITH_LOCALS", default=True, cast=bool)
SENTRY_MAX_BREADCRUMBS = config("SENTRY_MAX_BREADCRUMBS", default=100, cast=int)
SENTRY_BEFORE_SEND_TRANSACTION = config("SENTRY_BEFORE_SEND_TRANSACTION", default=None)

# Event filtering
SENTRY_IGNORE_ERRORS = [
    "django.security.DisallowedHost",
    "django.core.exceptions.PermissionDenied",
    "django.http.Http404",
    "rest_framework.exceptions.NotFound",
    "rest_framework.exceptions.PermissionDenied",
    "rest_framework.exceptions.NotAuthenticated",
]

# URL patterns to ignore
SENTRY_IGNORE_TRANSACTIONS = [
    "/health/",
    "/healthcheck/",
    "/metrics/",
    "/readiness/",
    "/liveness/",
]

# Sensitive data patterns to scrub
SENTRY_SCRUB_DEFAULTS = True
SENTRY_SCRUB_DATA = True
SENTRY_SCRUB_IP_ADDRESS = False  # Set to True to anonymize IP addresses
SENTRY_SCRUB_FIELDS = [
    "password",
    "secret",
    "token",
    "api_key",
    "apikey",
    "access_token",
    "refresh_token",
    "private_key",
    "ssn",
    "social_security_number",
    "credit_card",
    "card_number",
    "cvv",
    "pin",
]

# Integrations configuration
sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture all INFO-level logs and above
    event_level=logging.ERROR,  # Send only ERROR-level logs to Sentry
)

django_integration = DjangoIntegration(
    transaction_style="url",
    middleware_spans=True,
    signals_spans=True,
    cache_spans=True,
)

celery_integration = CeleryIntegration(
    monitor_beat_tasks=True,
    propagate_traces=True,
)

redis_integration = RedisIntegration()


def before_send(event, hint):
    """
    Custom filtering logic before sending events to Sentry.
    This function is called for every event before it's sent.
    """
    # Filter out specific errors
    if "exc_info" in hint:
        exc_type, exc_value, tb = hint["exc_info"]
        if exc_type.__name__ in SENTRY_IGNORE_ERRORS:
            return None

    # Filter out specific URLs
    if event.get("request") and event["request"].get("url"):
        url = event["request"]["url"]
        parsed_url = urlparse(url)
        for pattern in SENTRY_IGNORE_TRANSACTIONS:
            if pattern in parsed_url.path:
                return None

    # Additional custom filtering
    # Example: Filter by user
    if event.get("user") and event["user"].get("email"):
        if event["user"]["email"].endswith("@test.com"):
            return None  # Don't send events from test users

    # Scrub additional sensitive data
    if SENTRY_SCRUB_DATA and event.get("extra"):
        for field in SENTRY_SCRUB_FIELDS:
            if field in event["extra"]:
                event["extra"][field] = "[Filtered]"

    return event


def before_send_transaction(event, hint):
    """
    Custom filtering logic for performance transactions.
    """
    # Filter out specific transaction names
    transaction_name = event.get("transaction")
    if transaction_name:
        for pattern in SENTRY_IGNORE_TRANSACTIONS:
            if pattern in transaction_name:
                return None

    # Example: Sample transactions based on custom logic
    # Only send 10% of successful transactions, but 100% of slow ones
    if event.get("contexts", {}).get("trace", {}).get("status") == "ok":
        if (
            event.get("timestamp") - event.get("start_timestamp", 0) < 1.0
        ):  # Fast transaction
            import random

            if random.random() > 0.1:  # Only send 10%
                return None

    return event


def configure_sentry():
    """Initialize Sentry for error tracking and performance monitoring."""
    if not SENTRY_DSN:
        logger.warning("Sentry DSN not set, skipping Sentry setup.")
        return False

    try:
        # Get additional context
        server_name = os.environ.get("HOSTNAME", None)

        sentry_sdk.init(
            dsn=SENTRY_DSN,
            environment=SENTRY_ENVIRONMENT,
            release=SENTRY_RELEASE,
            # Integrations
            integrations=[
                django_integration,
                celery_integration,
                redis_integration,
                sentry_logging,
            ],
            # Performance monitoring
            traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
            profiles_sample_rate=SENTRY_PROFILES_SAMPLE_RATE,
            _experiments={
                "continuous_profiling_auto_start": True,
            },
            # Data handling
            send_default_pii=SENTRY_SEND_DEFAULT_PII,
            attach_stacktrace=SENTRY_ATTACH_STACKTRACE,
            request_bodies=SENTRY_REQUEST_BODIES,
            with_locals=SENTRY_WITH_LOCALS,
            max_breadcrumbs=SENTRY_MAX_BREADCRUMBS,
            # Filtering
            before_send=before_send,
            before_send_transaction=(
                before_send_transaction if SENTRY_TRACES_SAMPLE_RATE > 0 else None
            ),
            ignore_errors=SENTRY_IGNORE_ERRORS,
            # Debug
            debug=SENTRY_DEBUG,
            # Server name
            server_name=server_name,
            # Additional options
            shutdown_timeout=10,
            include_local_variables=SENTRY_WITH_LOCALS,
            include_source_context=True,
        )

        # Set user context if available
        from django.contrib.auth import get_user_model

        get_user_model()

        # Configure scope defaults
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag("app", "sol-web")
            scope.set_context(
                "app_info",
                {
                    "environment": SENTRY_ENVIRONMENT,
                    "release": SENTRY_RELEASE,
                    "python_version": os.sys.version,
                },
            )

        logger.info(
            "Sentry configured successfully",
            environment=SENTRY_ENVIRONMENT,
            release=SENTRY_RELEASE,
            traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
        )
        return True

    except Exception as e:
        logger.error(f"Failed to configure Sentry: {str(e)}")
        return False


# Custom context processors
def sentry_set_user_context(user):
    """Set user context for Sentry."""
    if not user or not user.is_authenticated:
        sentry_sdk.set_user(None)
        return

    sentry_sdk.set_user(
        {
            "id": user.id,
            "email": user.email,
            "username": getattr(user, "username", user.email),
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
    )


def sentry_set_transaction_name(name):
    """Set custom transaction name."""
    with sentry_sdk.configure_scope() as scope:
        scope.set_transaction_name(name)


def sentry_add_breadcrumb(message, category=None, level="info", data=None):
    """Add a breadcrumb to the current scope."""
    sentry_sdk.add_breadcrumb(
        message=message,
        category=category,
        level=level,
        data=data or {},
    )


def sentry_capture_message(message, level="info", **kwargs):
    """Capture a message to Sentry."""
    return sentry_sdk.capture_message(message, level=level, **kwargs)


def sentry_capture_exception(exception, **kwargs):
    """Capture an exception to Sentry."""
    return sentry_sdk.capture_exception(exception, **kwargs)


# Performance monitoring helpers
def sentry_start_transaction(name, op="http.server", **kwargs):
    """Start a performance transaction."""
    return sentry_sdk.start_transaction(name=name, op=op, **kwargs)


def sentry_start_span(op, description=None, **kwargs):
    """Start a performance span."""
    return sentry_sdk.start_span(op=op, description=description, **kwargs)


# Initialize Sentry
TEST_MODE = config("TEST_MODE", default=False, cast=bool)
SENTRY_FORCE_DISABLE = config("SENTRY_FORCE_DISABLE", default=False, cast=bool)

if not TEST_MODE and not SENTRY_FORCE_DISABLE:
    sentry_configured = configure_sentry()
else:
    logger.info(
        "Sentry initialization skipped",
        test_mode=TEST_MODE,
        force_disable=SENTRY_FORCE_DISABLE,
    )
