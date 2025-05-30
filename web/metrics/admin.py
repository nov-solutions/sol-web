from django.contrib import admin
from django.utils.html import format_html

from .models import MetricEvent, ServiceHealthCheck


@admin.register(MetricEvent)
class MetricEventAdmin(admin.ModelAdmin):
    list_display = ["name", "metric_type", "value", "timestamp", "get_labels_display"]
    list_filter = ["metric_type", "name", "timestamp"]
    search_fields = ["name", "description"]
    readonly_fields = ["timestamp"]
    date_hierarchy = "timestamp"

    fieldsets = (
        (None, {"fields": ("name", "metric_type", "value", "description")}),
        ("Metadata", {"fields": ("labels", "timestamp"), "classes": ("collapse",)}),
    )

    def get_labels_display(self, obj):
        if obj.labels:
            return format_html(
                "<code>{}</code>", ", ".join(f"{k}={v}" for k, v in obj.labels.items())
            )
        return "-"

    get_labels_display.short_description = "Labels"


@admin.register(ServiceHealthCheck)
class ServiceHealthCheckAdmin(admin.ModelAdmin):
    list_display = [
        "service_name",
        "get_status_display",
        "response_time_ms",
        "checked_at",
    ]
    list_filter = ["status", "service_name", "checked_at"]
    search_fields = ["service_name", "error_message"]
    readonly_fields = ["checked_at"]
    date_hierarchy = "checked_at"

    fieldsets = (
        (None, {"fields": ("service_name", "status", "response_time_ms")}),
        (
            "Details",
            {
                "fields": ("error_message", "metadata", "checked_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_status_display(self, obj):
        colors = {"healthy": "green", "unhealthy": "red", "degraded": "orange"}
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, "black"),
            obj.get_status_display(),
        )

    get_status_display.short_description = "Status"

    def has_add_permission(self, request):
        # Health checks should only be created by the system
        return False
