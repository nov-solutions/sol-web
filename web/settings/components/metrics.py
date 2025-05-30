import os

# Metrics configuration for Prometheus integration

# Enable/disable metrics collection
METRICS_ENABLED = os.environ.get("METRICS_ENABLED", "True").lower() == "true"

# Metrics endpoint authentication
# Option 1: IP-based authentication (for Prometheus server)
METRICS_ALLOWED_IPS = os.environ.get("METRICS_ALLOWED_IPS", "127.0.0.1,::1").split(",")

# Option 2: Token-based authentication
METRICS_AUTH_TOKEN = os.environ.get("METRICS_AUTH_TOKEN", None)

# Paths to exclude from metrics collection
METRICS_EXCLUDE_PATHS = [
    "/metrics/",
    "/health/",
    "/readiness/",
    "/liveness/",
    "/static/",
    "/media/",
]

# Prometheus multiprocess mode (for gunicorn/uwsgi)
# Set this to a writable directory when using multiple workers
PROMETHEUS_MULTIPROC_DIR = os.environ.get("PROMETHEUS_MULTIPROC_DIR", None)

# Custom metrics configuration
METRICS_CUSTOM_LABELS = {
    "app": os.environ.get("APP_NAME", "sol-web"),
    "environment": os.environ.get("ENVIRONMENT", "development"),
    "version": os.environ.get("APP_VERSION", "1.0.0"),
}

# Metrics export interval (for background tasks)
METRICS_EXPORT_INTERVAL = int(os.environ.get("METRICS_EXPORT_INTERVAL", "60"))

# Database metrics
METRICS_TRACK_DB_QUERIES = (
    os.environ.get("METRICS_TRACK_DB_QUERIES", "True").lower() == "true"
)

# Cache metrics
METRICS_TRACK_CACHE = os.environ.get("METRICS_TRACK_CACHE", "True").lower() == "true"

# Celery metrics
METRICS_TRACK_CELERY = os.environ.get("METRICS_TRACK_CELERY", "True").lower() == "true"

# Health check configuration
HEALTH_CHECK_CACHE_KEY = "health_check_status"
HEALTH_CHECK_CACHE_TIMEOUT = 60  # seconds

# Performance thresholds for health checks
HEALTH_CHECK_DB_TIMEOUT = 5.0  # seconds
HEALTH_CHECK_CACHE_TIMEOUT = 2.0  # seconds
HEALTH_CHECK_REDIS_TIMEOUT = 2.0  # seconds

# Metrics storage settings (optional - for storing metrics in database)
METRICS_STORE_IN_DB = os.environ.get("METRICS_STORE_IN_DB", "False").lower() == "true"
METRICS_RETENTION_DAYS = int(os.environ.get("METRICS_RETENTION_DAYS", "7"))

# Grafana/Prometheus URLs (for documentation/dashboards)
PROMETHEUS_URL = os.environ.get("PROMETHEUS_URL", "http://localhost:9090")
GRAFANA_URL = os.environ.get("GRAFANA_URL", "http://localhost:3000")
