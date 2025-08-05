from datetime import datetime

import stripe
import structlog
from django.conf import settings

logger = structlog.get_logger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


def _convert_timestamp_to_datetime(timestamp):
    """Convert Unix timestamp to datetime object if not None"""
    return datetime.fromtimestamp(timestamp) if timestamp is not None else None


class StripeSessionService:
    @staticmethod
    def create_subscription_checkout_session(
        connected_account_id: str,
        amount: int,
        interval: str,
        success_url: str,
        cancel_url: str,
        customer_email: str = None,
        customer_id: str = None,
    ):
        """
        Create a Checkout Session for subscription creation on the platform
        that routes subscription funds to the connected Express account.
        """
        session_params = {
            "mode": "subscription",
            "ui_mode": "hosted",
            "submit_type": "donate",
            "payment_method_types": ["card", "us_bank_account"],
            "success_url": success_url,
            "cancel_url": cancel_url,
            "billing_address_collection": "required",
            "line_items": [
                {
                    "price_data": {
                        "product_data": {
                            "name": "President's Associates Membership",
                        },
                        "unit_amount": amount,
                        "currency": "usd",
                        "recurring": {
                            "interval": interval,
                        },
                    },
                    "quantity": 1,
                }
            ],
            "subscription_data": {
                "on_behalf_of": connected_account_id,
                "transfer_data": {"destination": connected_account_id},
                "metadata": {
                    "connected_account_id": connected_account_id,
                    "created_via": "platform_checkout",
                },
                "application_fee_percent": settings.APPLICATION_FEE_PERCENT,
            },
        }

        if customer_id:
            session_params["customer"] = customer_id
        else:
            if customer_email:
                session_params["customer_email"] = customer_email

        return stripe.checkout.Session.create(**session_params)

    @staticmethod
    def create_payment_checkout_session(
        connected_account_id: str,
        amount: int,
        success_url: str,
        cancel_url: str,
        customer_email: str = None,
        customer_id: str = None,
    ):
        """
        Create a Checkout Session for one-time payment on the platform
        that routes payment funds to the connected Express account.
        """
        session_params = {
            "mode": "payment",
            "ui_mode": "hosted",
            "submit_type": "donate",
            "billing_address_collection": "required",
            "payment_method_types": ["card", "us_bank_account"],
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [
                {
                    "price_data": {
                        "product_data": {
                            "name": "President's Associates Donation",
                        },
                        "unit_amount": amount,
                        "currency": "usd",
                    },
                    "quantity": 1,
                }
            ],
            "payment_intent_data": {
                "on_behalf_of": connected_account_id,
                "transfer_data": {"destination": connected_account_id},
                "metadata": {
                    "connected_account_id": connected_account_id,
                    "created_via": "platform_checkout",
                },
                "application_fee_amount": int(
                    (amount * ((settings.APPLICATION_FEE_PERCENT) / 100))
                ),
            },
        }

        if customer_id:
            session_params["customer"] = customer_id
        else:
            if customer_email:
                session_params["customer_email"] = customer_email
                session_params["customer_creation"] = "always"

        return stripe.checkout.Session.create(**session_params)

    @staticmethod
    def create_billing_portal_session(
        customer_id: str, return_url: str, account_id: str
    ):
        """
        Create a customer portal session for subscription management.
        This allows customers to update payment methods, cancel subscriptions, etc.
        """
        return stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=return_url,
            on_behalf_of=account_id,
        )

    @staticmethod
    def create_connected_account_session(connected_account_id: str):
        """
        Create a login link for a connected account.
        """
        return stripe.Account.create_login_link(connected_account_id)


class ConnectedAccountService:
    # TODO: this needs to reworked into separate fetch and format methods
    @staticmethod
    def refresh_connected_account_data_from_stripe(account_id: str) -> dict:
        """Retrieve connected account details."""
        account = stripe.Account.retrieve(account_id)
        account_data = {
            "stripe_id": account.get("id", None),
            "details_submitted": account.get("details_submitted", None),
            "charges_enabled": account.get("charges_enabled", None),
            "branding_icon_file_id": account.get("settings", {})
            .get("branding", {})
            .get("icon", None),
            "branding_logo_file_id": account.get("settings", {})
            .get("branding", {})
            .get("logo", None),
            "branding_primary_color": account.get("settings", {})
            .get("branding", {})
            .get("primary_color", None),
            "branding_secondary_color": account.get("settings", {})
            .get("branding", {})
            .get("secondary_color", None),
            "name": account.get("business_profile", {}).get("name", None),
        }
        return account_data


class CustomerService:
    @staticmethod
    def format_customer_data_from_stripe(customer_data: dict) -> tuple[dict, str]:
        """Format customer data from Stripe"""
        address = customer_data.get("address") or {}

        return {
            "email": customer_data.get("email", None),
            "name": customer_data.get("name", None),
            "phone": customer_data.get("phone", None),
            "city": address.get("city", None),
            "country": address.get("country", None),
            "line1": address.get("line1", None),
            "line2": address.get("line2", None),
            "postal_code": address.get("postal_code", None),
            "state": address.get("state", None),
            "metadata": dict(customer_data.get("metadata", {})),
        }, customer_data.get("id", None)

    @staticmethod
    def refresh_customer_data_from_stripe(customer_id: str) -> dict:
        """Refresh customer data from Stripe"""
        customer = stripe.Customer.retrieve(customer_id)
        data, _ = CustomerService.format_customer_data_from_stripe(customer)
        return data


class SubscriptionService:
    @staticmethod
    def format_subscription_data_from_stripe(subscription_data: dict) -> dict:
        """Format subscription data from Stripe"""

        subscription_details = {
            "customer_id": subscription_data.get("customer", None),
            "status": subscription_data.get("status", None),
            "start_date": _convert_timestamp_to_datetime(
                subscription_data.get("start_date", None)
            ),
            "next_pending_invoice_item_invoice": _convert_timestamp_to_datetime(
                subscription_data.get("next_pending_invoice_item_invoice", None)
            ),
            "billing_cycle_anchor": _convert_timestamp_to_datetime(
                subscription_data.get("billing_cycle_anchor", None)
            ),
            "current_period_end": _convert_timestamp_to_datetime(
                subscription_data.get("current_period_end", None)
            ),
            "cancel_at_period_end": subscription_data.get("cancel_at_period_end", None),
            "cancel_at": _convert_timestamp_to_datetime(
                subscription_data.get("cancel_at", None)
            ),
            "connected_account_id": dict(subscription_data.get("metadata", {})).get(
                "connected_account_id", None
            ),
        }

        recurring_obj = (
            subscription_data.get("items", {})
            .get("data", [{}])[0]
            .get("price", {})
            .get("recurring", {})
        )

        recurring_details = {
            "interval": recurring_obj.get("interval", None),
            "interval_count": recurring_obj.get("interval_count", None),
        }

        return {
            **subscription_details,
            **recurring_details,
        }, subscription_data.get("id", None)

    @staticmethod
    def refresh_subscription_data_from_stripe(subscription_id: str) -> dict:
        """Refresh subscription data from Stripe"""
        subscription = stripe.Subscription.retrieve(subscription_id)
        subscription_data, _ = SubscriptionService.format_subscription_data_from_stripe(
            subscription
        )

        return subscription_data


class InvoiceService:
    @staticmethod
    def format_invoice_data_from_stripe(invoice_data: dict) -> tuple[dict, str]:
        """Format invoice data from Stripe"""
        return {
            "customer_id": invoice_data.get("customer", None),
            "subscription_id": invoice_data.get("subscription", None),
            "connected_account_id": invoice_data.get("on_behalf_of", None),
            "description": invoice_data.get("description", None),
            "billing_reason": invoice_data.get("billing_reason", None),
            "amount_paid": invoice_data.get("amount_paid", 0),
            "currency": invoice_data.get("currency", "usd"),
            "invoice_pdf": invoice_data.get("invoice_pdf", None),
            "hosted_invoice_url": invoice_data.get("hosted_invoice_url", None),
            "status": invoice_data.get("status", "draft"),
            "period_start": _convert_timestamp_to_datetime(
                invoice_data.get("period_start", None)
            ),
            "period_end": _convert_timestamp_to_datetime(
                invoice_data.get("period_end", None)
            ),
        }, invoice_data.get("id", None)

    @staticmethod
    def refresh_invoice_data_from_stripe(invoice_id: str) -> dict:
        """Refresh invoice data from Stripe"""
        invoice = stripe.Invoice.retrieve(invoice_id)
        invoice_data, _ = InvoiceService.format_invoice_data_from_stripe(invoice)
        return invoice_data
