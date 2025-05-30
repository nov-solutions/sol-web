from django.contrib import admin
from django.utils.html import format_html

from .models import (
    StripeCustomer,
    StripePayment,
    StripePaymentMethod,
    StripePrice,
    StripeProduct,
    StripeSubscription,
    StripeWebhookEvent,
)


@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = ["user", "stripe_customer_id", "email", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__email", "stripe_customer_id", "email"]
    readonly_fields = ["stripe_customer_id", "created_at", "updated_at"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


@admin.register(StripeProduct)
class StripeProductAdmin(admin.ModelAdmin):
    list_display = ["name", "stripe_product_id", "active", "created_at"]
    list_filter = ["active", "created_at"]
    search_fields = ["name", "stripe_product_id"]
    readonly_fields = ["stripe_product_id", "created_at", "updated_at"]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ["stripe_product_id"]
        return self.readonly_fields


@admin.register(StripePrice)
class StripePriceAdmin(admin.ModelAdmin):
    list_display = [
        "get_display_name",
        "stripe_price_id",
        "active",
        "unit_amount_display",
        "currency",
        "recurring_interval",
    ]
    list_filter = ["active", "currency", "recurring_interval", "created_at"]
    search_fields = ["stripe_price_id", "product__name"]
    readonly_fields = ["stripe_price_id", "created_at", "updated_at"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")

    def get_display_name(self, obj):
        return str(obj)

    get_display_name.short_description = "Price"

    def unit_amount_display(self, obj):
        return f"${obj.display_price:.2f}"

    unit_amount_display.short_description = "Amount"

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ["stripe_price_id", "product"]
        return self.readonly_fields


@admin.register(StripeSubscription)
class StripeSubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "get_customer_email",
        "get_product_name",
        "status",
        "current_period_end",
        "cancel_at_period_end",
    ]
    list_filter = ["status", "cancel_at_period_end", "created_at"]
    search_fields = [
        "stripe_subscription_id",
        "customer__user__email",
        "price__product__name",
    ]
    readonly_fields = ["stripe_subscription_id", "created_at", "updated_at"]
    date_hierarchy = "created_at"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("customer__user", "price__product")
        )

    def get_customer_email(self, obj):
        return obj.customer.user.email

    get_customer_email.short_description = "Customer"
    get_customer_email.admin_order_field = "customer__user__email"

    def get_product_name(self, obj):
        return obj.price.product.name if obj.price else "-"

    get_product_name.short_description = "Product"
    get_product_name.admin_order_field = "price__product__name"


@admin.register(StripePaymentMethod)
class StripePaymentMethodAdmin(admin.ModelAdmin):
    list_display = [
        "get_customer_email",
        "type",
        "brand",
        "last4",
        "is_default",
        "created_at",
    ]
    list_filter = ["type", "is_default", "brand", "created_at"]
    search_fields = ["stripe_payment_method_id", "customer__user__email", "last4"]
    readonly_fields = ["stripe_payment_method_id", "created_at", "updated_at"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("customer__user")

    def get_customer_email(self, obj):
        return obj.customer.user.email

    get_customer_email.short_description = "Customer"
    get_customer_email.admin_order_field = "customer__user__email"


@admin.register(StripePayment)
class StripePaymentAdmin(admin.ModelAdmin):
    list_display = [
        "stripe_payment_intent_id",
        "get_customer_email",
        "amount_display",
        "status",
        "created_at",
    ]
    list_filter = ["status", "currency", "created_at"]
    search_fields = ["stripe_payment_intent_id", "customer__user__email", "description"]
    readonly_fields = ["stripe_payment_intent_id", "created_at", "updated_at"]
    date_hierarchy = "created_at"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("customer__user")

    def get_customer_email(self, obj):
        return obj.customer.user.email

    get_customer_email.short_description = "Customer"
    get_customer_email.admin_order_field = "customer__user__email"

    def amount_display(self, obj):
        return f"${obj.display_amount:.2f} {obj.currency.upper()}"

    amount_display.short_description = "Amount"


@admin.register(StripeWebhookEvent)
class StripeWebhookEventAdmin(admin.ModelAdmin):
    list_display = [
        "stripe_event_id",
        "type",
        "processed",
        "processed_at",
        "created_at",
    ]
    list_filter = ["type", "processed", "created_at"]
    search_fields = ["stripe_event_id", "type"]
    readonly_fields = [
        "stripe_event_id",
        "type",
        "data",
        "processed",
        "processed_at",
        "error",
        "created_at",
    ]
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def data_preview(self, obj):
        import json

        data_str = json.dumps(obj.data, indent=2)
        if len(data_str) > 500:
            data_str = data_str[:500] + "..."
        return format_html("<pre>{}</pre>", data_str)

    data_preview.short_description = "Data"
