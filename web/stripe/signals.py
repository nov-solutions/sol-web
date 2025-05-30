from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import get_or_create_stripe_customer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_stripe_customer_on_user_creation(sender, instance, created, **kwargs):
    """
    Create a Stripe customer when a new user is created.
    This can be disabled by setting STRIPE_AUTO_CREATE_CUSTOMER = False
    """
    if created and getattr(settings, "STRIPE_AUTO_CREATE_CUSTOMER", True):
        if hasattr(instance, "stripe_customer"):
            return  # Customer already exists

        try:
            get_or_create_stripe_customer(instance)
        except Exception as e:
            # Log the error but don't prevent user creation
            import logging

            logger = logging.getLogger(__name__)
            logger.error(
                f"Failed to create Stripe customer for user {instance.id}: {str(e)}"
            )
