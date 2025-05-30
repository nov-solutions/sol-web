from django.apps import AppConfig


class MetricsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "metrics"
    verbose_name = "Metrics"

    def ready(self):
        # Import signal handlers and register collectors
        from . import collectors  # noqa
