import logging
from typing import Callable, Dict, Optional

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .models import ConnectedAccount, Customer, Invoice, Subscription
from .utils import CustomerUtils, InvoiceUtils, SubscriptionUtils

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


class WebhookHandler:
    def __init__(self, event):
        """
        Initialize webhook handler from a pre-verified event
        """
        logger.info(f"Handling webhook event of type: {event.type}")

        self.event = event
        self.event_type: str = event.type
        self.event_data: dict = event.data.object

    def handle(self) -> None:
        """Main handler that routes events to appropriate methods"""
        handler = self._get_handler()
        if handler:
            handler()
        else:
            logger.info(f"Unhandled event type: {self.event_type}")

    def _get_handler(self) -> Optional[Callable]:
        """Maps event types to their handler methods"""
        handlers: Dict[str, Callable] = {
            "customer.subscription.created": self.handle_subscription_created,
            "customer.subscription.updated": self.handle_subscription_updated,
            "customer.subscription.deleted": self.handle_subscription_deleted,
            "checkout.session.completed": self.handle_checkout_session_completed,
            "invoice.paid": self.handle_invoice_paid,
            "customer.created": self.handle_customer_created,
            "customer.updated": self.handle_customer_updated,
            "customer.deleted": self.handle_customer_deleted,
            "customer.subscription.trial_will_end": self.handle_subscription_trial_will_end,
            "invoice.payment_succeeded": self.handle_invoice_payment_succeeded,
            "invoice.payment_failed": self.handle_invoice_payment_failed,
        }
        return handlers.get(self.event_type)

    # TODO: likely needs to reworked, included as placeholder for now
    def handle_subscription_trial_will_end(self):
        logger.info(
            f"Subscription trial will end: {self.event_data.get('subscription')}"
        )
        subscription_id = self.event_data.get("subscription")
        subscription = Subscription.objects.get(stripe_subscription_id=subscription_id)
        subscription.refresh_data_from_stripe()
        logger.info(f"Subscription refreshed after trial will end: {subscription_id}")

    # TODO: likely needs to reworked, included as placeholder for now
    def handle_invoice_payment_failed(self):
        logger.info(
            f"Payment failed for subscription: {self.event_data.get('subscription')}"
        )
        subscription_id = self.event_data.get("subscription")
        subscription = Subscription.objects.get(stripe_subscription_id=subscription_id)
        subscription.refresh_data_from_stripe()
        logger.info(f"Subscription refreshed after payment failure: {subscription_id}")

    # TODO: likely needs to reworked, included as placeholder for now
    def handle_invoice_payment_succeeded(self):
        logger.info(
            f"Payment succeeded for subscription: {self.event_data.get('subscription')}"
        )
        subscription_id = self.event_data.get("subscription")
        subscription = Subscription.objects.get(stripe_subscription_id=subscription_id)
        subscription.refresh_data_from_stripe()
        logger.info(f"Subscription refreshed after payment success: {subscription_id}")

    def handle_checkout_session_completed(self) -> None:
        """Handle successful checkout - important for initial subscription creation"""
        logger.info(f"Checkout completed: {self.event_data.get('id')}")

        subscription_id = self.event_data.get("subscription", None)
        customer_id = self.event_data.get("customer", None)

        if customer_id and subscription_id:
            customer, _ = Customer.objects.get_or_create(stripe_customer_id=customer_id)
            customer.refresh_data_from_stripe()
            subscription, _ = Subscription.objects.get_or_create(
                stripe_subscription_id=subscription_id
            )
            subscription.refresh_data_from_stripe()

            logger.info(f"Subscription customer updated: {subscription_id}")
        else:
            logger.warning(
                f"Checkout completed, but customer or subscription not found: {self.event_data}"
            )

    def handle_subscription_created(self) -> None:
        """Handle new subscription creation"""
        subscription_data, subscription_id = (
            SubscriptionUtils.format_subscription_data_from_stripe(self.event_data)
        )

        try:
            Customer.objects.get(
                stripe_customer_id=subscription_data.get("customer_id")
            )
        except Customer.DoesNotExist:
            logger.warning(
                f"Customer not found for subscription, skipping creation: {subscription_id}"
            )
            return

        try:
            _, created = Subscription.objects.get_or_create(
                stripe_id=subscription_id, defaults=subscription_data
            )
            if created:
                logger.info(f"Subscription created: {subscription_id}")
            else:
                logger.info(f"Subscription already exists, skipping: {subscription_id}")
        except Exception as e:
            logger.error(f"Error handling subscription creation: {str(e)}")

    def handle_subscription_updated(self) -> None:
        """Handle subscription updates (status changes, plan changes, etc.)"""
        subscription_data, subscription_id = (
            SubscriptionUtils.format_subscription_data_from_stripe(self.event_data)
        )

        try:
            Customer.objects.get(
                stripe_customer_id=subscription_data.get("customer_id")
            )
        except Customer.DoesNotExist:
            logger.warning(
                f"Customer not found for subscription, skipping update or creation: {subscription_id}"
            )
            return

        try:
            Subscription.objects.update_or_create(
                stripe_id=subscription_id, **subscription_data
            )
            logger.info(f"Subscription updated: {subscription_id}")
        except Exception as e:
            logger.error(f"Error handling subscription update: {str(e)}")

    def handle_subscription_deleted(self) -> None:
        """Handle subscription cancellation/deletion"""
        subscription_data, subscription_id = (
            SubscriptionUtils.format_subscription_data_from_stripe(self.event_data)
        )
        try:
            Subscription.objects.update(
                stripe_subscription_id=subscription_id, **subscription_data
            )
            logger.info(f"Subscription canceled: {subscription_id}")
        except Exception as e:
            logger.error(f"Error handling subscription deletion: {str(e)}")

    def handle_invoice_paid(self) -> None:
        """Handle invoice paid event - creates or updates invoice record"""
        invoice_data, invoice_id = InvoiceUtils.format_invoice_data_from_stripe(
            self.event_data
        )

        try:
            customer = Customer.objects.get(
                stripe_customer_id=invoice_data.get("customer_id")
            )

            subscription = None
            if invoice_data.get("subscription_id"):
                try:
                    subscription = Subscription.objects.get(
                        stripe_subscription_id=invoice_data.get("subscription_id")
                    )
                except Subscription.DoesNotExist:
                    logger.warning(f"Subscription not found for invoice: {invoice_id}")

            connected_account = None
            if invoice_data.get("connected_account_id"):
                try:
                    connected_account = ConnectedAccount.objects.get(
                        stripe_connected_account_id=invoice_data.get(
                            "connected_account_id"
                        )
                    )
                except ConnectedAccount.DoesNotExist:
                    logger.warning(
                        f"Connected account not found for invoice: {invoice_id}"
                    )

            _, created = Invoice.objects.update_or_create(
                stripe_id=invoice_id,
                defaults={
                    "customer": customer,
                    "subscription": subscription,
                    "connected_account": connected_account,
                    "description": invoice_data.get("lines", {})
                    .get("data", [{}])[0]
                    .get("description", None),
                    "billing_reason": invoice_data.get("billing_reason"),
                    "amount_paid": invoice_data.get("amount_paid"),
                    "currency": invoice_data.get("currency"),
                    "invoice_pdf": invoice_data.get("invoice_pdf"),
                    "hosted_invoice_url": invoice_data.get("hosted_invoice_url"),
                    "status": invoice_data.get("status"),
                    "period_start": invoice_data.get("period_start"),
                    "period_end": invoice_data.get("period_end"),
                },
            )

            if created:
                logger.info(f"Invoice created: {invoice_id}")
            else:
                logger.info(f"Invoice updated: {invoice_id}")

        except Customer.DoesNotExist:
            logger.warning(f"Customer not found for invoice, skipping: {invoice_id}")
        except Exception as e:
            logger.error(f"Error handling invoice paid event: {str(e)}")

    def handle_customer_created(self) -> None:
        """Handle customer creation"""
        customer_data, customer_id = CustomerUtils.format_customer_data_from_stripe(
            self.event_data
        )
        try:
            Customer.objects.update_or_create(
                stripe_customer_id=customer_id,
                **customer_data,
            )
            logger.info(f"Customer created: {customer_id}")
        except Exception as e:
            logger.error(f"Error handling customer creation: {str(e)}")

    def handle_customer_updated(self) -> None:
        """Handle customer update"""
        customer_data, customer_id = CustomerUtils.format_customer_data_from_stripe(
            self.event_data
        )
        try:
            Customer.objects.update(
                stripe_customer_id=customer_id,
                **customer_data,
            )
            logger.info(f"Customer updated: {customer_id}")
        except Exception as e:
            logger.error(f"Customer data: {customer_data}, ID: {customer_id}")
            logger.error(f"Error handling customer update: {str(e)}")

    def handle_customer_deleted(self) -> None:
        """Handle customer deletion"""
        customer_id = self.event_data.get("id")
        try:
            Customer.objects.get(stripe_customer_id=customer_id).delete()
            logger.info(f"Customer deleted: {customer_id}")
        except Exception as e:
            logger.error(f"Error handling customer deletion: {str(e)}")


@csrf_exempt
@api_view(["POST"])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
        handler = WebhookHandler(event)
        handler.handle()
        return HttpResponse(status=200)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        logger.error(f"Webhook signature verification failed: {e}")
        return HttpResponse(status=400)
    except Exception as e:
        logger.error(f"Webhook handler error: {str(e)}")
        return HttpResponse(status=500)
