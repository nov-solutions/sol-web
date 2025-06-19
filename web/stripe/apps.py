from django.apps import AppConfig


class StripeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stripe"
    verbose_name = "Stripe"
