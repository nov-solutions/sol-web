from django.conf import settings
from django.db import models
from django.utils import timezone


class StripeCustomer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stripe_customer",
    )
    stripe_customer_id = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "stripe_customers"
        verbose_name = "Stripe Customer"
        verbose_name_plural = "Stripe Customers"

    def __str__(self):
        return f"{self.user.email} - {self.stripe_customer_id}"


class StripeProduct(models.Model):
    stripe_product_id = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "stripe_products"
        verbose_name = "Stripe Product"
        verbose_name_plural = "Stripe Products"

    def __str__(self):
        return self.name


class StripePrice(models.Model):
    RECURRING_INTERVAL_CHOICES = [
        ("day", "Day"),
        ("week", "Week"),
        ("month", "Month"),
        ("year", "Year"),
    ]

    stripe_price_id = models.CharField(max_length=255, unique=True, db_index=True)
    product = models.ForeignKey(
        StripeProduct, on_delete=models.CASCADE, related_name="prices"
    )
    active = models.BooleanField(default=True)
    currency = models.CharField(max_length=3, default="usd")
    unit_amount = models.IntegerField(help_text="Amount in cents")
    recurring_interval = models.CharField(
        max_length=10, choices=RECURRING_INTERVAL_CHOICES, blank=True, null=True
    )
    recurring_interval_count = models.IntegerField(default=1, blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "stripe_prices"
        verbose_name = "Stripe Price"
        verbose_name_plural = "Stripe Prices"

    def __str__(self):
        amount = self.unit_amount / 100
        interval = f"/{self.recurring_interval}" if self.recurring_interval else ""
        return f"{self.product.name} - ${amount:.2f}{interval}"

    @property
    def display_price(self):
        return self.unit_amount / 100


class StripeSubscription(models.Model):
    STATUS_CHOICES = [
        ("trialing", "Trialing"),
        ("active", "Active"),
        ("incomplete", "Incomplete"),
        ("incomplete_expired", "Incomplete Expired"),
        ("past_due", "Past Due"),
        ("canceled", "Canceled"),
        ("unpaid", "Unpaid"),
    ]

    stripe_subscription_id = models.CharField(
        max_length=255, unique=True, db_index=True
    )
    customer = models.ForeignKey(
        StripeCustomer, on_delete=models.CASCADE, related_name="subscriptions"
    )
    price = models.ForeignKey(
        StripePrice, on_delete=models.SET_NULL, null=True, related_name="subscriptions"
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    cancel_at_period_end = models.BooleanField(default=False)
    canceled_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    trial_start = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "stripe_subscriptions"
        verbose_name = "Stripe Subscription"
        verbose_name_plural = "Stripe Subscriptions"

    def __str__(self):
        return f"{self.customer.user.email} - {self.price.product.name} ({self.status})"

    @property
    def is_active(self):
        return self.status in ["active", "trialing"]


class StripePaymentMethod(models.Model):
    TYPE_CHOICES = [
        ("card", "Card"),
        ("bank_account", "Bank Account"),
        ("paypal", "PayPal"),
    ]

    stripe_payment_method_id = models.CharField(
        max_length=255, unique=True, db_index=True
    )
    customer = models.ForeignKey(
        StripeCustomer, on_delete=models.CASCADE, related_name="payment_methods"
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    is_default = models.BooleanField(default=False)
    brand = models.CharField(max_length=50, blank=True)
    last4 = models.CharField(max_length=4, blank=True)
    exp_month = models.IntegerField(null=True, blank=True)
    exp_year = models.IntegerField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "stripe_payment_methods"
        verbose_name = "Stripe Payment Method"
        verbose_name_plural = "Stripe Payment Methods"

    def __str__(self):
        if self.type == "card":
            return f"{self.brand} ****{self.last4}"
        return f"{self.type} - {self.stripe_payment_method_id}"


class StripePayment(models.Model):
    STATUS_CHOICES = [
        ("requires_payment_method", "Requires Payment Method"),
        ("requires_confirmation", "Requires Confirmation"),
        ("requires_action", "Requires Action"),
        ("processing", "Processing"),
        ("requires_capture", "Requires Capture"),
        ("canceled", "Canceled"),
        ("succeeded", "Succeeded"),
    ]

    stripe_payment_intent_id = models.CharField(
        max_length=255, unique=True, db_index=True
    )
    customer = models.ForeignKey(
        StripeCustomer, on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.IntegerField(help_text="Amount in cents")
    currency = models.CharField(max_length=3, default="usd")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    description = models.TextField(blank=True)
    payment_method = models.ForeignKey(
        StripePaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "stripe_payments"
        verbose_name = "Stripe Payment"
        verbose_name_plural = "Stripe Payments"

    def __str__(self):
        amount = self.amount / 100
        return f"{self.customer.user.email} - ${amount:.2f} ({self.status})"

    @property
    def display_amount(self):
        return self.amount / 100


class StripeWebhookEvent(models.Model):
    stripe_event_id = models.CharField(max_length=255, unique=True, db_index=True)
    type = models.CharField(max_length=255, db_index=True)
    data = models.JSONField()
    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "stripe_webhook_events"
        verbose_name = "Stripe Webhook Event"
        verbose_name_plural = "Stripe Webhook Events"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.type} - {self.stripe_event_id}"

    def mark_processed(self):
        self.processed = True
        self.processed_at = timezone.now()
        self.save(update_fields=["processed", "processed_at"])
