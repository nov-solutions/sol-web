"""
Prometheus metric collectors for Django application monitoring.
"""

import platform

from django.conf import settings
from django.db import connection
from prometheus_client import Counter, Gauge, Histogram, Info

# Application Info
app_info = Info(
    "django_app",
    "Django application information",
)
app_info.info(
    {
        "version": getattr(settings, "APP_VERSION", "unknown"),
        "environment": getattr(settings, "ENVIRONMENT", "unknown"),
        "python_version": platform.python_version(),
        "django_version": "4.2",
    }
)

# Request metrics
http_requests_total = Counter(
    "django_http_requests_total",
    "Total HTTP requests",
    ["method", "view", "status"],
)

http_request_duration_seconds = Histogram(
    "django_http_request_duration_seconds",
    "HTTP request latency",
    ["method", "view"],
)

http_requests_in_progress = Gauge(
    "django_http_requests_in_progress",
    "HTTP requests in progress",
)

http_request_size_bytes = Histogram(
    "django_http_request_size_bytes",
    "HTTP request size in bytes",
    ["method", "view"],
)

http_response_size_bytes = Histogram(
    "django_http_response_size_bytes",
    "HTTP response size in bytes",
    ["method", "view", "status"],
)

# Database metrics
db_connections_total = Gauge(
    "django_db_connections_total",
    "Total database connections",
)

db_queries_total = Counter(
    "django_db_queries_total",
    "Total database queries",
    ["operation"],  # SELECT, INSERT, UPDATE, DELETE
)

db_query_duration_seconds = Histogram(
    "django_db_query_duration_seconds",
    "Database query duration",
    ["operation"],
)

# Cache metrics
cache_hits_total = Counter(
    "django_cache_hits_total",
    "Total cache hits",
    ["backend"],
)

cache_misses_total = Counter(
    "django_cache_misses_total",
    "Total cache misses",
    ["backend"],
)

cache_sets_total = Counter(
    "django_cache_sets_total",
    "Total cache sets",
    ["backend"],
)

cache_deletes_total = Counter(
    "django_cache_deletes_total",
    "Total cache deletes",
    ["backend"],
)

# Celery metrics (if using Celery)
celery_tasks_total = Counter(
    "django_celery_tasks_total",
    "Total Celery tasks",
    ["task", "status"],  # status: pending, success, failure, retry
)

celery_task_duration_seconds = Histogram(
    "django_celery_task_duration_seconds",
    "Celery task duration",
    ["task"],
)

celery_queue_length = Gauge(
    "django_celery_queue_length",
    "Celery queue length",
    ["queue"],
)

# Business metrics
user_registrations_total = Counter(
    "django_user_registrations_total",
    "Total user registrations",
)

user_logins_total = Counter(
    "django_user_logins_total",
    "Total user logins",
    ["method"],  # password, social, sso
)

active_users_total = Gauge(
    "django_active_users_total",
    "Total active users",
)

# System metrics
process_memory_bytes = Gauge(
    "django_process_memory_bytes",
    "Process memory usage in bytes",
)

process_cpu_percent = Gauge(
    "django_process_cpu_percent",
    "Process CPU usage percentage",
)

process_threads_total = Gauge(
    "django_process_threads_total",
    "Total process threads",
)

process_open_files_total = Gauge(
    "django_process_open_files_total",
    "Total open file descriptors",
)

python_gc_collections_total = Counter(
    "django_python_gc_collections_total",
    "Total Python garbage collections",
    ["generation"],
)

# Custom business metrics - extend these based on your needs
custom_metric_counter = Counter(
    "django_custom_metric_total",
    "Custom business metric counter",
    ["type", "action"],
)

custom_metric_gauge = Gauge(
    "django_custom_metric_current",
    "Custom business metric gauge",
    ["type"],
)


def collect_db_metrics():
    """Collect database metrics."""
    try:
        # Get connection count
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT count(*) FROM pg_stat_activity WHERE datname = current_database();"
            )
            count = cursor.fetchone()[0]
            db_connections_total.set(count)
    except Exception:
        pass  # Fail silently


def increment_request_metric(method, view_name, status_code):
    """Increment request counter."""
    http_requests_total.labels(
        method=method, view=view_name, status=str(status_code)
    ).inc()


def observe_request_duration(method, view_name, duration):
    """Observe request duration."""
    http_request_duration_seconds.labels(method=method, view=view_name).observe(
        duration
    )


def track_cache_operation(operation, backend="default", hit=None):
    """Track cache operations."""
    if operation == "get":
        if hit:
            cache_hits_total.labels(backend=backend).inc()
        else:
            cache_misses_total.labels(backend=backend).inc()
    elif operation == "set":
        cache_sets_total.labels(backend=backend).inc()
    elif operation == "delete":
        cache_deletes_total.labels(backend=backend).inc()


def track_user_activity(activity_type, **kwargs):
    """Track user-related activities."""
    if activity_type == "registration":
        user_registrations_total.inc()
    elif activity_type == "login":
        method = kwargs.get("method", "password")
        user_logins_total.labels(method=method).inc()


def track_custom_metric(metric_type, action, value=1, gauge_value=None):
    """Track custom business metrics."""
    custom_metric_counter.labels(type=metric_type, action=action).inc(value)
    if gauge_value is not None:
        custom_metric_gauge.labels(type=metric_type).set(gauge_value)


# Initialize system metrics collection
def initialize_metrics():
    """Initialize metrics collection."""
    collect_db_metrics()
