from django.db import models
from django.utils import timezone


class MetricEvent(models.Model):
    """
    Model to store custom metric events for tracking and analysis.
    This is optional - you can use Prometheus without storing metrics in DB.
    """

    METRIC_TYPES = [
        ("counter", "Counter"),
        ("gauge", "Gauge"),
        ("histogram", "Histogram"),
        ("summary", "Summary"),
    ]

    name = models.CharField(max_length=255, db_index=True)
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES)
    value = models.FloatField()
    labels = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "metrics_events"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["name", "-timestamp"]),
            models.Index(fields=["metric_type", "name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.metric_type}): {self.value}"


class ServiceHealthCheck(models.Model):
    """
    Model to track health check results for various services.
    """

    STATUS_CHOICES = [
        ("healthy", "Healthy"),
        ("unhealthy", "Unhealthy"),
        ("degraded", "Degraded"),
    ]

    service_name = models.CharField(max_length=100, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    response_time_ms = models.FloatField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    checked_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = "metrics_health_checks"
        ordering = ["-checked_at"]
        indexes = [
            models.Index(fields=["service_name", "-checked_at"]),
        ]

    def __str__(self):
        return f"{self.service_name}: {self.status} at {self.checked_at}"
