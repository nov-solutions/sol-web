import logging

from django.utils import timezone

from .models import (
    StripeCustomer,
    StripePayment,
    StripePaymentMethod,
    StripePrice,
    StripeProduct,
    StripeSubscription,
    StripeWebhookEvent,
)

logger = logging.getLogger(__name__)


def webhook_handler(event):
    """Main webhook handler that routes events to specific handlers"""

    # Store the webhook event
    webhook_event, created = StripeWebhookEvent.objects.get_or_create(
        stripe_event_id=event["id"],
        defaults={
            "type": event["type"],
            "data": event["data"],
        },
    )

    if not created and webhook_event.processed:
        logger.info(f"Event {event['id']} already processed")
        return

    try:
        # Route to specific handlers
        handlers = {
            "customer.created": handle_customer_created,
            "customer.updated": handle_customer_updated,
            "customer.deleted": handle_customer_deleted,
            "customer.subscription.created": handle_subscription_created,
            "customer.subscription.updated": handle_subscription_updated,
            "customer.subscription.deleted": handle_subscription_deleted,
            "invoice.payment_succeeded": handle_invoice_payment_succeeded,
            "invoice.payment_failed": handle_invoice_payment_failed,
            "payment_intent.succeeded": handle_payment_intent_succeeded,
            "payment_intent.payment_failed": handle_payment_intent_failed,
            "payment_method.attached": handle_payment_method_attached,
            "payment_method.detached": handle_payment_method_detached,
            "product.created": handle_product_created,
            "product.updated": handle_product_updated,
            "product.deleted": handle_product_deleted,
            "price.created": handle_price_created,
            "price.updated": handle_price_updated,
            "price.deleted": handle_price_deleted,
        }

        handler = handlers.get(event["type"])
        if handler:
            handler(event)
        else:
            logger.info(f"Unhandled event type: {event['type']}")

        webhook_event.mark_processed()

    except Exception as e:
        logger.error(f"Error processing webhook {event['id']}: {str(e)}")
        webhook_event.error = str(e)
        webhook_event.save()
        raise


def handle_customer_created(event):
    """Handle customer.created webhook"""
    stripe_customer = event["data"]["object"]
    logger.info(f"Customer created: {stripe_customer['id']}")


def handle_customer_updated(event):
    """Handle customer.updated webhook"""
    stripe_customer = event["data"]["object"]

    try:
        customer = StripeCustomer.objects.get(stripe_customer_id=stripe_customer["id"])
        customer.email = stripe_customer.get("email", customer.email)
        customer.save()
        logger.info(f"Customer updated: {stripe_customer['id']}")
    except StripeCustomer.DoesNotExist:
        logger.warning(f"Customer not found: {stripe_customer['id']}")


def handle_customer_deleted(event):
    """Handle customer.deleted webhook"""
    stripe_customer = event["data"]["object"]

    try:
        customer = StripeCustomer.objects.get(stripe_customer_id=stripe_customer["id"])
        customer.delete()
        logger.info(f"Customer deleted: {stripe_customer['id']}")
    except StripeCustomer.DoesNotExist:
        logger.warning(f"Customer not found for deletion: {stripe_customer['id']}")


def handle_subscription_created(event):
    """Handle customer.subscription.created webhook"""
    stripe_subscription = event["data"]["object"]

    try:
        customer = StripeCustomer.objects.get(
            stripe_customer_id=stripe_subscription["customer"]
        )
        price = StripePrice.objects.get(
            stripe_price_id=stripe_subscription["items"]["data"][0]["price"]["id"]
        )

        subscription, created = StripeSubscription.objects.update_or_create(
            stripe_subscription_id=stripe_subscription["id"],
            defaults={
                "customer": customer,
                "price": price,
                "status": stripe_subscription["status"],
                "current_period_start": timezone.datetime.fromtimestamp(
                    stripe_subscription["current_period_start"], tz=timezone.utc
                ),
                "current_period_end": timezone.datetime.fromtimestamp(
                    stripe_subscription["current_period_end"], tz=timezone.utc
                ),
                "cancel_at_period_end": stripe_subscription["cancel_at_period_end"],
                "canceled_at": (
                    timezone.datetime.fromtimestamp(
                        stripe_subscription["canceled_at"], tz=timezone.utc
                    )
                    if stripe_subscription["canceled_at"]
                    else None
                ),
                "trial_start": (
                    timezone.datetime.fromtimestamp(
                        stripe_subscription["trial_start"], tz=timezone.utc
                    )
                    if stripe_subscription["trial_start"]
                    else None
                ),
                "trial_end": (
                    timezone.datetime.fromtimestamp(
                        stripe_subscription["trial_end"], tz=timezone.utc
                    )
                    if stripe_subscription["trial_end"]
                    else None
                ),
                "metadata": stripe_subscription.get("metadata", {}),
            },
        )

        action = "created" if created else "updated"
        logger.info(f"Subscription {action}: {stripe_subscription['id']}")

    except StripeCustomer.DoesNotExist:
        logger.error(f"Customer not found: {stripe_subscription['customer']}")
    except StripePrice.DoesNotExist:
        logger.error(
            f"Price not found: {stripe_subscription['items']['data'][0]['price']['id']}"
        )


def handle_subscription_updated(event):
    """Handle customer.subscription.updated webhook"""
    handle_subscription_created(event)  # Same logic for update


def handle_subscription_deleted(event):
    """Handle customer.subscription.deleted webhook"""
    stripe_subscription = event["data"]["object"]

    try:
        subscription = StripeSubscription.objects.get(
            stripe_subscription_id=stripe_subscription["id"]
        )
        subscription.status = "canceled"
        subscription.ended_at = timezone.now()
        subscription.save()
        logger.info(f"Subscription canceled: {stripe_subscription['id']}")
    except StripeSubscription.DoesNotExist:
        logger.warning(f"Subscription not found: {stripe_subscription['id']}")


def handle_invoice_payment_succeeded(event):
    """Handle invoice.payment_succeeded webhook"""
    invoice = event["data"]["object"]
    logger.info(f"Invoice payment succeeded: {invoice['id']}")

    # Update subscription if it exists
    if invoice["subscription"]:
        try:
            subscription = StripeSubscription.objects.get(
                stripe_subscription_id=invoice["subscription"]
            )
            subscription.status = "active"
            subscription.save()
        except StripeSubscription.DoesNotExist:
            logger.warning(f"Subscription not found: {invoice['subscription']}")


def handle_invoice_payment_failed(event):
    """Handle invoice.payment_failed webhook"""
    invoice = event["data"]["object"]
    logger.warning(f"Invoice payment failed: {invoice['id']}")

    # Update subscription status if it exists
    if invoice["subscription"]:
        try:
            subscription = StripeSubscription.objects.get(
                stripe_subscription_id=invoice["subscription"]
            )
            subscription.status = "past_due"
            subscription.save()
        except StripeSubscription.DoesNotExist:
            logger.warning(f"Subscription not found: {invoice['subscription']}")


def handle_payment_intent_succeeded(event):
    """Handle payment_intent.succeeded webhook"""
    payment_intent = event["data"]["object"]

    try:
        customer = StripeCustomer.objects.get(
            stripe_customer_id=payment_intent["customer"]
        )

        payment, created = StripePayment.objects.update_or_create(
            stripe_payment_intent_id=payment_intent["id"],
            defaults={
                "customer": customer,
                "amount": payment_intent["amount"],
                "currency": payment_intent["currency"],
                "status": payment_intent["status"],
                "description": payment_intent.get("description", ""),
                "metadata": payment_intent.get("metadata", {}),
            },
        )

        logger.info(f"Payment succeeded: {payment_intent['id']}")

    except StripeCustomer.DoesNotExist:
        logger.error(f"Customer not found: {payment_intent['customer']}")


def handle_payment_intent_failed(event):
    """Handle payment_intent.payment_failed webhook"""
    payment_intent = event["data"]["object"]

    try:
        payment = StripePayment.objects.get(
            stripe_payment_intent_id=payment_intent["id"]
        )
        payment.status = "failed"
        payment.save()
        logger.warning(f"Payment failed: {payment_intent['id']}")
    except StripePayment.DoesNotExist:
        logger.warning(f"Payment not found: {payment_intent['id']}")


def handle_payment_method_attached(event):
    """Handle payment_method.attached webhook"""
    payment_method = event["data"]["object"]

    try:
        customer = StripeCustomer.objects.get(
            stripe_customer_id=payment_method["customer"]
        )

        pm, created = StripePaymentMethod.objects.update_or_create(
            stripe_payment_method_id=payment_method["id"],
            defaults={
                "customer": customer,
                "type": payment_method["type"],
                "brand": (
                    payment_method["card"]["brand"]
                    if payment_method["type"] == "card"
                    else ""
                ),
                "last4": (
                    payment_method["card"]["last4"]
                    if payment_method["type"] == "card"
                    else ""
                ),
                "exp_month": (
                    payment_method["card"]["exp_month"]
                    if payment_method["type"] == "card"
                    else None
                ),
                "exp_year": (
                    payment_method["card"]["exp_year"]
                    if payment_method["type"] == "card"
                    else None
                ),
                "metadata": payment_method.get("metadata", {}),
            },
        )

        logger.info(f"Payment method attached: {payment_method['id']}")

    except StripeCustomer.DoesNotExist:
        logger.error(f"Customer not found: {payment_method['customer']}")


def handle_payment_method_detached(event):
    """Handle payment_method.detached webhook"""
    payment_method = event["data"]["object"]

    try:
        pm = StripePaymentMethod.objects.get(
            stripe_payment_method_id=payment_method["id"]
        )
        pm.delete()
        logger.info(f"Payment method detached: {payment_method['id']}")
    except StripePaymentMethod.DoesNotExist:
        logger.warning(f"Payment method not found: {payment_method['id']}")


def handle_product_created(event):
    """Handle product.created webhook"""
    stripe_product = event["data"]["object"]

    product, created = StripeProduct.objects.update_or_create(
        stripe_product_id=stripe_product["id"],
        defaults={
            "name": stripe_product["name"],
            "description": stripe_product.get("description", ""),
            "active": stripe_product["active"],
            "metadata": stripe_product.get("metadata", {}),
        },
    )

    logger.info(f"Product created: {stripe_product['id']}")


def handle_product_updated(event):
    """Handle product.updated webhook"""
    handle_product_created(event)  # Same logic for update


def handle_product_deleted(event):
    """Handle product.deleted webhook"""
    stripe_product = event["data"]["object"]

    try:
        product = StripeProduct.objects.get(stripe_product_id=stripe_product["id"])
        product.active = False
        product.save()
        logger.info(f"Product deactivated: {stripe_product['id']}")
    except StripeProduct.DoesNotExist:
        logger.warning(f"Product not found: {stripe_product['id']}")


def handle_price_created(event):
    """Handle price.created webhook"""
    stripe_price = event["data"]["object"]

    try:
        product = StripeProduct.objects.get(stripe_product_id=stripe_price["product"])

        price, created = StripePrice.objects.update_or_create(
            stripe_price_id=stripe_price["id"],
            defaults={
                "product": product,
                "active": stripe_price["active"],
                "currency": stripe_price["currency"],
                "unit_amount": stripe_price["unit_amount"],
                "recurring_interval": (
                    stripe_price["recurring"]["interval"]
                    if stripe_price.get("recurring")
                    else None
                ),
                "recurring_interval_count": (
                    stripe_price["recurring"]["interval_count"]
                    if stripe_price.get("recurring")
                    else None
                ),
                "metadata": stripe_price.get("metadata", {}),
            },
        )

        logger.info(f"Price created: {stripe_price['id']}")

    except StripeProduct.DoesNotExist:
        logger.error(f"Product not found: {stripe_price['product']}")


def handle_price_updated(event):
    """Handle price.updated webhook"""
    handle_price_created(event)  # Same logic for update


def handle_price_deleted(event):
    """Handle price.deleted webhook"""
    stripe_price = event["data"]["object"]

    try:
        price = StripePrice.objects.get(stripe_price_id=stripe_price["id"])
        price.active = False
        price.save()
        logger.info(f"Price deactivated: {stripe_price['id']}")
    except StripePrice.DoesNotExist:
        logger.warning(f"Price not found: {stripe_price['id']}")
