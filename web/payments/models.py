from django.conf import settings
from django.db import models
from django.utils import timezone

from .services import ConnectedAccountService, CustomerService, SubscriptionService


class ConnectedAccount(models.Model):
    stripe_connected_account_id = models.CharField(
        max_length=255, unique=True, db_index=True
    )
    name = models.CharField(max_length=255, null=True, blank=True)

    charges_enabled = models.BooleanField(default=False)
    details_submitted = models.BooleanField(default=False)

    branding_icon_file_id = models.CharField(max_length=255, null=True, blank=True)
    branding_logo_file_id = models.CharField(max_length=255, null=True, blank=True)
    branding_primary_color = models.CharField(max_length=7, null=True, blank=True)
    branding_secondary_color = models.CharField(max_length=7, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def refresh_data_from_stripe(self):
        """Refresh data from Stripe"""
        account_data = (
            ConnectedAccountService.refresh_connected_account_data_from_stripe(
                self.stripe_connected_account_id
            )
        )
        self.charges_enabled = account_data.get("charges_enabled", False)
        self.details_submitted = account_data.get("details_submitted", False)
        self.branding_icon_file_id = account_data.get("branding_icon_file_id", None)
        self.branding_logo_file_id = account_data.get("branding_logo_file_id", None)
        self.branding_primary_color = account_data.get("branding_primary_color", None)
        self.branding_secondary_color = account_data.get(
            "branding_secondary_color", None
        )
        self.name = account_data.get("name", None)
        self.save(
            update_fields=[
                "charges_enabled",
                "details_submitted",
                "branding_icon_file_id",
                "branding_logo_file_id",
                "branding_primary_color",
                "branding_secondary_color",
                "name",
            ]
        )

    def __str__(self):
        return f"{self.name} - {self.stripe_connected_account_id}"


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stripe_customer",
    )
    stripe_customer_id = models.CharField(max_length=255, unique=True, db_index=True)

    email = models.EmailField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    line1 = models.CharField(max_length=255, null=True, blank=True)
    line2 = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)

    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def refresh_data_from_stripe(self):
        """Refresh data from Stripe"""
        customer_data = CustomerService.refresh_customer_data_from_stripe(
            self.stripe_customer_id
        )
        self.email = customer_data.get("email", None)
        self.name = customer_data.get("name", None)
        self.phone = customer_data.get("phone", None)
        self.city = customer_data.get("city", None)
        self.country = customer_data.get("country", None)
        self.line1 = customer_data.get("line1", None)
        self.line2 = customer_data.get("line2", None)
        self.postal_code = customer_data.get("postal_code", None)
        self.state = customer_data.get("state", None)
        self.metadata = customer_data.get("metadata", {})
        self.save(
            update_fields=[
                "email",
                "name",
                "phone",
                "city",
                "country",
                "line1",
                "line2",
                "postal_code",
                "state",
                "metadata",
            ]
        )

    def __str__(self):
        return f"{self.user.email} - {self.stripe_customer_id}"

    @property
    def has_active_subscription(self):
        """Check if customer has any active subscription"""
        return self.subscriptions.filter(status__in=["active", "trialing"]).exists()

    @property
    def active_subscription(self):
        """Get the current active subscription (if any)"""
        return self.subscriptions.filter(status__in=["active", "trialing"]).first()


class Subscription(models.Model):
    STATUS_CHOICES = [
        ("incomplete", "Incomplete"),
        ("trialing", "Trialing"),
        ("active", "Active"),
        ("past_due", "Past Due"),
        ("canceled", "Canceled"),
        ("unpaid", "Unpaid"),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="subscriptions"
    )
    stripe_subscription_id = models.CharField(
        max_length=255, unique=True, db_index=True
    )
    connected_account = models.ForeignKey(
        "ConnectedAccount",
        on_delete=models.CASCADE,
        related_name="subscriptions",
        null=True,
        blank=True,
    )
    stripe_price_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, db_index=True)

    start_date = models.DateTimeField(null=True, blank=True)
    interval = models.CharField(max_length=255, null=True, blank=True)
    interval_count = models.IntegerField(null=True, blank=True)

    next_pending_invoice_item_invoice = models.DateTimeField(null=True, blank=True)
    billing_cycle_anchor = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField()
    cancel_at_period_end = models.BooleanField(default=False)
    cancel_at = models.DateTimeField(null=True, blank=True)

    trial_end = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def refresh_data_from_stripe(self):
        """Refresh data from Stripe"""
        subscription_data = SubscriptionService.refresh_subscription_data_from_stripe(
            self.stripe_subscription_id
        )
        self.status = subscription_data.get("status", None)
        self.start_date = subscription_data.get("start_date", None)
        self.interval = subscription_data.get("interval", None)
        self.interval_count = subscription_data.get("interval_count", None)
        self.next_pending_invoice_item_invoice = subscription_data.get(
            "next_pending_invoice_item_invoice", None
        )
        self.billing_cycle_anchor = subscription_data.get("billing_cycle_anchor", None)
        self.current_period_end = subscription_data.get("current_period_end", None)
        self.cancel_at_period_end = subscription_data.get("cancel_at_period_end", False)
        self.cancel_at = subscription_data.get("cancel_at", None)
        self.save(
            update_fields=[
                "status",
                "start_date",
                "interval",
                "interval_count",
                "next_pending_invoice_item_invoice",
                "billing_cycle_anchor",
                "current_period_end",
                "cancel_at_period_end",
                "cancel_at",
            ]
        )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer.user.email} - {self.status}"

    @property
    def is_active(self):
        """Check if subscription is currently active"""
        return self.status in ["active", "trialing"]

    @property
    def is_trialing(self):
        """Check if subscription is in trial period"""
        return (
            self.status == "trialing"
            and self.trial_end
            and self.trial_end > timezone.now()
        )

    @property
    def days_until_period_end(self):
        """Days remaining in current billing period"""
        if self.current_period_end:
            delta = self.current_period_end - timezone.now()
            return max(0, delta.days)
        return 0


class Invoice(models.Model):
    stripe_invoice_id = models.CharField(max_length=255, unique=True, db_index=True)
    customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, related_name="invoices"
    )
    connected_account = models.ForeignKey(
        "ConnectedAccount", on_delete=models.CASCADE, related_name="invoices"
    )
    subscription = models.ForeignKey(
        "Subscription",
        on_delete=models.SET_NULL,
        related_name="invoices",
        null=True,
        blank=True,
    )

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("open", "Open"),
        ("paid", "Paid"),
        ("uncollectible", "Uncollectible"),
        ("void", "Void"),
    ]
    BILLING_REASON_CHOICES = [
        ("manual", "Manual"),
        (
            "automatic_pending_invoice_item_invoice",
            "Automatic Pending Invoice Item Invoice",
        ),
        ("upcoming", "Upcoming"),
        ("subscription_create", "Subscription Create"),
        ("subscription_update", "Subscription Update"),
        ("subscription_cycle", "Subscription Cycle"),
        ("subscription_threshold", "Subscription Threshold"),
    ]
    description = models.CharField(max_length=255, null=True, blank=True)
    billing_reason = models.CharField(max_length=40, choices=BILLING_REASON_CHOICES)
    amount_paid = models.BigIntegerField()
    currency = models.CharField(max_length=10)
    invoice_pdf = models.URLField(max_length=800, null=True, blank=True)
    hosted_invoice_url = models.URLField(max_length=800, null=True, blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)

    period_start = models.DateTimeField(null=True, blank=True)
    period_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-period_end"]
        indexes = [
            models.Index(fields=["billing_reason"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"Invoice {self.stripe_id} ({self.get_billing_reason_display()})"
