from django.urls import path

from .views import (
    CreateCheckoutSessionView,
    CreatePortalSessionView,
    ListPaymentMethodsView,
    SetDefaultPaymentMethodView,
    billing_portal_return,
    checkout_cancel,
    checkout_success,
    stripe_webhook,
)

app_name = "stripe"

urlpatterns = [
    # Checkout
    path(
        "checkout/session/",
        CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path("checkout/success/", checkout_success, name="checkout-success"),
    path("checkout/cancel/", checkout_cancel, name="checkout-cancel"),
    # Customer Portal
    path(
        "portal/session/",
        CreatePortalSessionView.as_view(),
        name="create-portal-session",
    ),
    path("portal/return/", billing_portal_return, name="billing-portal-return"),
    # Payment Methods
    path(
        "payment-methods/",
        ListPaymentMethodsView.as_view(),
        name="list-payment-methods",
    ),
    path(
        "payment-methods/set-default/",
        SetDefaultPaymentMethodView.as_view(),
        name="set-default-payment-method",
    ),
    # Webhook
    path("webhook/", stripe_webhook, name="webhook"),
]
