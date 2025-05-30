from django.apps import AppConfig


class StripeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stripe"
    verbose_name = "Stripe"

    def ready(self):
        # Import signal handlers
        try:
            from . import signals  # noqa
        except ImportError:
            pass
