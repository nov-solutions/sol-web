"""
Custom Prometheus metrics collectors.
These metrics are automatically included in the /metrics endpoint.
"""

from django.urls import resolve
from prometheus_client import Counter, Gauge, Histogram

# Custom endpoint response time histogram
endpoint_response_time = Histogram(
    "django_endpoint_response_seconds",
    "Response time for specific endpoints",
    ["endpoint_name", "method", "status_code"],
    buckets=[
        0.005,
        0.01,
        0.025,
        0.05,
        0.075,
        0.1,
        0.25,
        0.5,
        0.75,
        1.0,
        2.5,
        5.0,
        7.5,
        10.0,
    ],
)

# Custom business metrics
user_actions_total = Counter(
    "django_user_actions_total", "Total user actions", ["action_type", "endpoint"]
)

active_users_gauge = Gauge(
    "django_active_users_current", "Current number of active users"
)

# Database operation metrics
db_operation_duration = Histogram(
    "django_db_operation_seconds",
    "Database operation duration",
    ["operation_type", "table"],
)

# Cache metrics
cache_operations_total = Counter(
    "django_cache_operations_total",
    "Total cache operations",
    ["operation", "cache_key_prefix"],
)


def get_endpoint_name(request):
    """Extract endpoint name from Django request."""
    try:
        resolver_match = resolve(request.path_info)
        if resolver_match.view_name:
            return resolver_match.view_name
        elif hasattr(resolver_match.func, "__name__"):
            return resolver_match.func.__name__
        else:
            return "unknown"
    except Exception:
        return "unknown"


def update_active_users(count):
    """Update active users gauge."""
    active_users_gauge.set(count)


def track_db_operation(operation_type, table_name, duration):
    """Track database operation duration."""
    db_operation_duration.labels(
        operation_type=operation_type, table=table_name
    ).observe(duration)


def track_cache_operation(operation, key_prefix):
    """Track cache operations."""
    cache_operations_total.labels(
        operation=operation, cache_key_prefix=key_prefix
    ).inc()
