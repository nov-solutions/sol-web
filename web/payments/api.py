import logging

import stripe
from core.pagination import StandardResultsSetPagination
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ConnectedAccount, Customer, Invoice, Subscription
from .serializers import (
    ConnectedAccountSerializer,
    CustomerSerializer,
    InvoiceSerializer,
    SubscriptionSerializer,
)
from .services import ConnectedAccountService, StripeSessionService

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


class BaseModelViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]


class ConnectedAccountViewSet(BaseModelViewSet):
    queryset = ConnectedAccount.objects.all()
    serializer_class = ConnectedAccountSerializer

    search_fields = ["stripe_connected_account_id"]

    def create(self, request):
        stripe_acct = ConnectedAccountService.create_connected_account()
        obj = ConnectedAccount.objects.create(
            stripe_id=stripe_acct.id,
            details_submitted=stripe_acct.details_submitted,
            charges_enabled=stripe_acct.charges_enabled,
        )
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def create_connected_account_session(self, request, pk=None):
        """Create an access link for the connected account."""
        connected_account = self.get_object()

        try:
            link = stripe.Account.create_login_link(connected_account.stripe_id)
            return Response(link.url, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # TODO: this needs to be reworked into its own viewset that doesn't utilize the ConnectedAccount pk field as it was removed
    # @action(detail=True, methods=["post"])
    # def update_branding(self, request, pk=None):
    #     """
    #     POST /payments/connected-accounts/<pk>/update_branding/

    #     Updates branding settings for a connected account, including file uploads for logo/icon.

    #     Body (multipart/form-data): {
    #         account_id: str,           # Connected account ID
    #         icon?: File,               # Icon file upload (optional)
    #         logo?: File,               # Logo file upload (optional)
    #         primary_color?: str,       # Hex color code (optional)
    #         secondary_color?: str      # Hex color code (optional)
    #     }
    #     """
    #     try:
    #         connected_account = self.get_object()

    #         icon_file = request.FILES.get("icon")
    #         logo_file = request.FILES.get("logo")
    #         primary_color = request.data.get("primary_color")
    #         secondary_color = request.data.get("secondary_color")

    #         if not any([icon_file, logo_file, primary_color, secondary_color]):
    #             return Response(
    #                 {"error": "At least one branding setting must be provided"},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )

    #         updated_account = ConnectedAccountService.update_account_branding(
    #             account_id=connected_account.stripe_id,
    #             icon_file=icon_file,
    #             logo_file=logo_file,
    #             primary_color=primary_color,
    #             secondary_color=secondary_color,
    #         )

    #         branding_info = {}
    #         if (
    #             hasattr(updated_account, "settings")
    #             and updated_account.settings.branding
    #         ):
    #             branding = updated_account.settings.branding
    #             branding_info = {
    #                 "icon": getattr(branding, "icon", None),
    #                 "logo": getattr(branding, "logo", None),
    #                 "primary_color": getattr(branding, "primary_color", None),
    #                 "secondary_color": getattr(branding, "secondary_color", None),
    #             }

    #         if branding_info.get("icon"):
    #             connected_account.branding_icon_file_id = branding_info["icon"]
    #         if branding_info.get("logo"):
    #             connected_account.branding_logo_file_id = branding_info["logo"]
    #         if branding_info.get("primary_color"):
    #             connected_account.branding_primary_color = branding_info[
    #                 "primary_color"
    #             ]
    #         if branding_info.get("secondary_color"):
    #             connected_account.branding_secondary_color = branding_info[
    #                 "secondary_color"
    #             ]

    #         connected_account.save()

    #         return Response(
    #             branding_info,
    #             status=status.HTTP_200_OK,
    #         )

    #     except ValueError as e:
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response(
    #             {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )


class CustomerViewSet(BaseModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    filterset_fields = ["country", "state"]
    search_fields = ["email", "name", "phone"]
    ordering_fields = ["name", "email"]
    ordering = ["name"]

    @action(detail=False, methods=["get"])
    def find_by_email(self, request):
        email = request.query_params.get("email")

        if not email:
            return Response(
                {"error": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        customer = self.queryset.filter(email__exact=email).first()

        if not customer:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(customer)
        return Response(serializer.data)


class SubscriptionViewSet(BaseModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    filterset_fields = [
        "status",
        "interval",
        "customer",
        "connected_account",
    ]
    search_fields = [
        "description",
        "stripe_subscription_id",
        "customer__email",
        "customer__name",
    ]
    ordering_fields = ["start_date", "status", "cancel_at"]


class InvoiceViewSet(BaseModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    filterset_fields = [
        "status",
        "billing_reason",
        "customer",
        "subscription",
        "connected_account",
    ]
    search_fields = [
        "description",
        "stripe_invoice_id",
        "customer__email",
        "customer__name",
    ]
    ordering_fields = ["period_start", "period_end", "status"]


class CheckoutSessionView(APIView):
    @action(detail=False, methods=["post"])
    def subscription(self, request):
        """
        POST /payments/checkout-sessions/subscription/

        Creates a Stripe Checkout Session for subscription creation using destination charges.

        Body: {
            connected_account_id: str,      # Connected account ID
            amount: int,          # Amount in cents for subscription
            interval?: str,        # Interval for subscription (month or year)
            customer_email?: str, # Email for new customer creation
            customer_id?: str,    # ID of existing customer to link
            success_url: str,     # URL to return to after checkout
            cancel_url: str,      # URL to return to if checkout is canceled
        }
        """
        try:
            connected_account_id = request.data.get("connected_account_id")
            amount = request.data.get("amount")
            interval = request.data.get("interval")
            customer_email = request.data.get("customer_email")
            customer_id = request.data.get("customer_id")
            success_url = request.data.get("success_url")
            cancel_url = request.data.get("cancel_url")

            if not all([connected_account_id, amount, success_url, cancel_url]):
                return Response(
                    {
                        "error": "connected_account_id, amount, success_url, and cancel_url are required"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if interval not in ["month", "year"]:
                return Response(
                    {"error": "interval must be 'month' or 'year'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            session = StripeSessionService.create_subscription_checkout_session(
                connected_account_id=connected_account_id,
                amount=amount,
                interval=interval,
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=customer_email,
                customer_id=customer_id,
            )

            return Response(
                {
                    "sessionId": session.id,
                    "clientSecret": session.client_secret,
                    "url": session.url,
                    "destinationAccount": connected_account_id,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["post"])
    def payment(self, request):
        """
        POST /payments/checkout-sessions/payment/

        Creates a Stripe Checkout Session for subscription creation using destination charges.

        Body: {
            connected_account_id: str,      # Connected account ID
            amount: int,          # Amount in cents for subscription
            customer_email?: str, # Email for new customer creation
            customer_id?: str,    # ID of existing customer to link
            success_url: str,     # URL to return to after checkout
            cancel_url: str,      # URL to return to if checkout is canceled
        }
        """
        try:
            connected_account_id = request.data.get("connected_account_id")
            amount = request.data.get("amount")
            success_url = request.data.get("success_url")
            cancel_url = request.data.get("cancel_url")

            if not all([connected_account_id, amount, success_url, cancel_url]):
                return Response(
                    {
                        "error": "connected_account_id, amount, success_url, and cancel_url are required"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            session = StripeSessionService.create_payment_checkout_session(
                connected_account_id=connected_account_id,
                amount=amount,
                success_url=success_url,
                cancel_url=cancel_url,
            )

            return Response(
                {
                    "sessionId": session.id,
                    "clientSecret": session.client_secret,
                    "url": session.url,
                    "destinationAccount": connected_account_id,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BillingPortalSessionView(APIView):
    def post(self, request):
        """
        POST /payments/billing-portal-sessions/

        Creates a customer portal session for subscription management.

        Args:
        - customer_id: str,
        - connected_account_id: str,
        """
        try:
            customer_id = request.data.get("customer_id")
            connected_account_id = request.data.get("connected_account_id")
            if not customer_id or not connected_account_id:
                return Response(
                    {"error": "customer_id and connected_account_id are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            portal_session = StripeSessionService.create_billing_portal_session(
                customer_id=customer_id,
                return_url=settings.STRIPE_RETURN_URL,
                account_id=connected_account_id,
            )

            return Response(
                {
                    "url": portal_session.url,
                    "customerId": customer_id,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ConnectedAccountSessionView(APIView):
    def post(self, request):
        """
        POST /payments/connected-account-sessions/
        """
        try:
            connected_account_id = request.data.get("connected_account_id")
            if not connected_account_id:
                return Response(
                    {"error": "connected_account_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            session = StripeSessionService.create_connected_account_session(
                connected_account_id=connected_account_id,
            )

            return Response(
                {"url": session.url},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
