from __future__ import absolute_import, unicode_literals

from celery import Celery
from celeryapp import celery_config

app = Celery("web")

app.config_from_object(celery_config)

# Import Sentry handlers if Sentry is configured
try:
    from django.conf import settings

    if hasattr(settings, "SENTRY_DSN") and settings.SENTRY_DSN:
        from . import sentry_handlers  # noqa: F401
except Exception:
    pass  # Sentry handlers are optional
