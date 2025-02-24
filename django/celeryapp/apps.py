import structlog

from django.apps import AppConfig

LOGGER = structlog.get_logger(__name__)


class CeleryIntegrationConfig(AppConfig):
    name = "celeryapp"

    def ready(self):
        LOGGER.info("CeleryIntegrationConfig ready() called. Importing tasks...")
