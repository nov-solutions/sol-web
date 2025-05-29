import structlog
from django.apps import AppConfig

logger = structlog.get_logger(__name__)


class CeleryAppConfig(AppConfig):
    name = "celeryapp"
    verbose_name = "Celery - Asynchronous Task Queue"

    def ready(self):
        logger.info("CeleryAppConfig ready() called. Importing tasks...")
