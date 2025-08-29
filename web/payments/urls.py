import api
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    cancel_subscription,
    create_checkout_session,
    create_portal_session,
    reactivate_subscription,
    subscription_status,
)
from .webhooks import stripe_webhook

app_name = "payments"

router = DefaultRouter()
router.register(
    r"connected-accounts", api.ConnectedAccountViewSet, basename="connected-accounts"
)
router.register(r"customers", api.CustomerViewSet, basename="customers")
router.register(r"subscriptions", api.SubscriptionViewSet, basename="subscriptions")
router.register(r"invoices", api.InvoiceViewSet, basename="invoices")

urlpatterns = [
    path("api/", include(router.urls)),
    # Sessions
    path(
        "api/sessions/checkout/",
        api.CheckoutSessionView.as_view(),
        name="checkout-sessions",
    ),
    path(
        "api/sessions/billing/",
        api.BillingPortalSessionView.as_view(),
        name="billing-sessions",
    ),
    path(
        "api/sessions/connected-account/",
        api.ConnectedAccountSessionView.as_view(),
        name="connected-account-sessions",
    ),
    # Subscription management
    path("checkout/", create_checkout_session, name="checkout"),
    path("portal/", create_portal_session, name="portal"),
    path("status/", subscription_status, name="status"),
    path("cancel/", cancel_subscription, name="cancel"),
    path("reactivate/", reactivate_subscription, name="reactivate"),
    # Webhook
    path("webhook/", stripe_webhook, name="webhook"),
]
