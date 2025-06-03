from django.apps import AppConfig


class MetricsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "metrics"
    verbose_name = "Metrics"

    def ready(self):
        # Import collectors to register them with prometheus
        from . import collectors  # noqa
