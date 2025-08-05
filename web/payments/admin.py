from django.contrib import admin
from django.utils.html import format_html

from .models import ConnectedAccount, Customer, Invoice, Subscription


@admin.register(ConnectedAccount)
class ConnectedAccountAdmin(admin.ModelAdmin):
    list_display = (
        "stripe_id",
        "name",
        "details_submitted",
        "charges_enabled",
    )
    list_filter = ("details_submitted", "charges_enabled")
    search_fields = ("stripe_id", "name")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "stripe_id",
                    "name",
                    "details_submitted",
                    "charges_enabled",
                    "branding_icon_file_id",
                    "branding_logo_file_id",
                    "branding_primary_color",
                    "branding_secondary_color",
                )
            },
        ),
        ("Metadata", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "user",
        "email",
        "stripe_customer_id",
        "has_active_sub",
        "created_at",
    ]
    search_fields = ["user__email", "name", "email", "stripe_customer_id"]
    readonly_fields = ["stripe_customer_id", "created_at", "updated_at"]
    fieldsets = (
        (
            "Customer",
            {
                "fields": (
                    "stripe_customer_id",
                    "email",
                    "name",
                    "phone",
                    "user",
                    "has_active_sub",
                )
            },
        ),
        (
            "Address",
            {
                "fields": (
                    "line1",
                    "line2",
                    "city",
                    "state",
                    "postal_code",
                    "country",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Stripe Metadata",
            {
                "fields": ("metadata",),
                "classes": ("collapse",),
            },
        ),
        ("Model Metadata", {"fields": ("created_at", "updated_at")}),
    )

    def has_active_sub(self, obj):
        """Show subscription status with color coding"""
        if obj.has_active_subscription:
            return format_html('<span style="color: green;">✓ Active</span>')
        return format_html('<span style="color: gray;">No subscription</span>')

    has_active_sub.short_description = "Subscription"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "customer",
        "status_colored",
        "stripe_price_id",
        "start_date",
        "current_period_end",
        "cancel_at_period_end",
        "created_at",
    ]
    list_filter = ["status", "cancel_at_period_end", "created_at"]
    search_fields = [
        "customer__name",
        "customer__email",
        "stripe_subscription_id",
        "stripe_price_id",
    ]
    readonly_fields = [
        "stripe_subscription_id",
        "created_at",
        "updated_at",
    ]
    ordering = ["-created_at"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "stripe_subscription_id",
                    "stripe_price_id",
                    "customer",
                    "status",
                )
            },
        ),
        (
            "Subscription Details",
            {
                "fields": (
                    "start_date",
                    "interval",
                    "interval_count",
                    "next_pending_invoice_item_invoice",
                    "billing_cycle_anchor",
                    "current_period_end",
                    "cancel_at_period_end",
                    "cancel_at",
                    "trial_end",
                ),
                "classes": ("collapse",),
            },
        ),
        ("Metadata", {"fields": ("created_at", "updated_at")}),
    )

    def status_colored(self, obj):
        """Show status with appropriate color"""
        colors = {
            "active": "green",
            "trialing": "blue",
            "past_due": "orange",
            "canceled": "red",
            "unpaid": "red",
        }
        color = colors.get(obj.status, "gray")
        return format_html(
            '<span style="color: {};">{}</span>', color, obj.get_status_display()
        )

    status_colored.short_description = "Status"
    status_colored.admin_order_field = "status"


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "stripe_invoice_id",
        "customer__name",
        "subscription__stripe_subscription_id",
        "status_colored",
        "amount_with_currency",
        "billing_reason_display",
        "period_end",
        "created_at",
    ]
    list_filter = ["status", "billing_reason", "currency"]
    search_fields = [
        "stripe_invoice_id",
        "customer__email",
        "customer__name",
        "description",
    ]
    readonly_fields = [
        "stripe_invoice_id",
        "created_at",
        "updated_at",
    ]
    ordering = ["-period_end", "-created_at"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "stripe_invoice_id",
                    "customer",
                    "subscription",
                    "connected_account",
                    "status",
                )
            },
        ),
        (
            "Invoice Details",
            {
                "fields": (
                    "description",
                    "billing_reason",
                    "amount_paid",
                    "currency",
                    "period_start",
                    "period_end",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "URLs",
            {
                "fields": (
                    "invoice_pdf",
                    "hosted_invoice_url",
                ),
                "classes": ("collapse",),
            },
        ),
        ("Metadata", {"fields": ("created_at", "updated_at")}),
    )

    def status_colored(self, obj):
        """Show status with appropriate color"""
        colors = {
            "draft": "gray",
            "open": "orange",
            "paid": "green",
            "uncollectible": "red",
            "void": "red",
        }
        color = colors.get(obj.status, "gray")
        return format_html(
            '<span style="color: {};">{}</span>', color, obj.get_status_display()
        )

    def amount_with_currency(self, obj):
        """Display amount with currency"""
        # Convert from cents to dollars/euros/etc
        amount = obj.amount_paid / 100.0
        return f"{obj.currency.upper()} {amount:.2f}"

    def billing_reason_display(self, obj):
        """Display shortened billing reason"""
        return obj.get_billing_reason_display()

    status_colored.short_description = "Status"
    status_colored.admin_order_field = "status"
    amount_with_currency.short_description = "Amount"
    billing_reason_display.short_description = "Billing Reason"
