import logging

import stripe
from django.conf import settings

from .models import StripeCustomer

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_or_create_stripe_customer(user):
    """Get or create a Stripe customer for a Django user"""
    try:
        return StripeCustomer.objects.get(user=user)
    except StripeCustomer.DoesNotExist:
        # Create customer in stripe
        stripe_customer = stripe.Customer.create(
            email=user.email,
            metadata={
                "user_id": str(user.id),
                "username": getattr(user, "username", ""),
            },
        )

        # Create customer in database
        customer = StripeCustomer.objects.create(
            user=user,
            stripe_customer_id=stripe_customer.id,
            email=user.email,
        )

        logger.info(f"Created Stripe customer {stripe_customer.id} for user {user.id}")
        return customer


def sync_stripe_products_and_prices():
    """Sync products and prices from Stripe to local database"""
    from .models import StripePrice, StripeProduct

    try:
        # Sync products
        products = stripe.Product.list(limit=100)
        for stripe_product in products.auto_paging_iter():
            product, created = StripeProduct.objects.update_or_create(
                stripe_product_id=stripe_product.id,
                defaults={
                    "name": stripe_product.name,
                    "description": stripe_product.get("description", ""),
                    "active": stripe_product.active,
                    "metadata": stripe_product.get("metadata", {}),
                },
            )
            action = "Created" if created else "Updated"
            logger.info(f"{action} product: {stripe_product.id}")

        # Sync prices
        prices = stripe.Price.list(limit=100)
        for stripe_price in prices.auto_paging_iter():
            try:
                product = StripeProduct.objects.get(
                    stripe_product_id=stripe_price.product
                )
                price, created = StripePrice.objects.update_or_create(
                    stripe_price_id=stripe_price.id,
                    defaults={
                        "product": product,
                        "active": stripe_price.active,
                        "currency": stripe_price.currency,
                        "unit_amount": stripe_price.unit_amount,
                        "recurring_interval": (
                            stripe_price.recurring.interval
                            if stripe_price.recurring
                            else None
                        ),
                        "recurring_interval_count": (
                            stripe_price.recurring.interval_count
                            if stripe_price.recurring
                            else None
                        ),
                        "metadata": stripe_price.get("metadata", {}),
                    },
                )
                action = "Created" if created else "Updated"
                logger.info(f"{action} price: {stripe_price.id}")
            except StripeProduct.DoesNotExist:
                logger.warning(
                    f"Product not found for price {stripe_price.id}: {stripe_price.product}"
                )

    except stripe.error.StripeError as e:
        logger.error(f"Stripe sync error: {str(e)}")
        raise


def cancel_subscription(subscription_id):
    """Cancel a subscription at period end"""
    try:
        stripe_subscription = stripe.Subscription.modify(
            subscription_id, cancel_at_period_end=True
        )

        # Update local record
        from .models import StripeSubscription

        try:
            subscription = StripeSubscription.objects.get(
                stripe_subscription_id=subscription_id
            )
            subscription.cancel_at_period_end = True
            subscription.save()
        except StripeSubscription.DoesNotExist:
            logger.warning(f"Local subscription not found: {subscription_id}")

        return stripe_subscription

    except stripe.error.StripeError as e:
        logger.error(f"Error canceling subscription: {str(e)}")
        raise


def reactivate_subscription(subscription_id):
    """Reactivate a canceled subscription"""
    try:
        stripe_subscription = stripe.Subscription.modify(
            subscription_id, cancel_at_period_end=False
        )

        # Update local record
        from .models import StripeSubscription

        try:
            subscription = StripeSubscription.objects.get(
                stripe_subscription_id=subscription_id
            )
            subscription.cancel_at_period_end = False
            subscription.save()
        except StripeSubscription.DoesNotExist:
            logger.warning(f"Local subscription not found: {subscription_id}")

        return stripe_subscription

    except stripe.error.StripeError as e:
        logger.error(f"Error reactivating subscription: {str(e)}")
        raise


def create_setup_intent(customer_id):
    """Create a setup intent for saving payment methods"""
    try:
        setup_intent = stripe.SetupIntent.create(
            customer=customer_id,
            payment_method_types=["card"],
        )
        return setup_intent
    except stripe.error.StripeError as e:
        logger.error(f"Error creating setup intent: {str(e)}")
        raise


def format_currency(amount_cents, currency="usd"):
    """Format currency amount for display"""
    amount = amount_cents / 100
    currency_symbols = {
        "usd": "$",
    }
    symbol = currency_symbols.get(currency.lower(), currency.upper() + " ")
    return f"{symbol}{amount:.2f}"
