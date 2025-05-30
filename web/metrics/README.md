# Metrics Module

This module provides comprehensive application monitoring using Prometheus metrics for Django applications.

## Features

- **Prometheus Integration**: Exposes metrics in Prometheus format at `/metrics/`
- **Request Tracking**: Automatic tracking of HTTP requests, response times, and sizes
- **Database Monitoring**: Track query counts and connection pool metrics
- **Cache Metrics**: Monitor cache hits, misses, and operations
- **System Metrics**: CPU, memory, threads, and file descriptor usage
- **Business Metrics**: Custom counters and gauges for application-specific metrics
- **Health Checks**: Kubernetes-compatible health, readiness, and liveness probes
- **Middleware Integration**: Automatic metric collection via Django middleware
- **Management Commands**: Export metrics and clean up old data

## Setup

### 1. Dependencies

Add to your `requirements.txt`:

```
prometheus-client>=0.19.0
psutil>=5.9.0
```

### 2. Configuration

The module is automatically configured if you're using the template structure. The settings are in `settings/components/metrics.py`.

### 3. Environment Variables

```bash
# Enable/disable metrics collection
METRICS_ENABLED=True

# Authentication
METRICS_ALLOWED_IPS=127.0.0.1,10.0.0.0/8
METRICS_AUTH_TOKEN=your-secret-token

# For multiprocess deployments (Gunicorn)
PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus_multiproc

# Optional: Store metrics in database
METRICS_STORE_IN_DB=False
METRICS_RETENTION_DAYS=7
```

## Usage

### Accessing Metrics

The metrics endpoint is available at `/metrics/`. Authentication is required:

1. **IP-based**: Configure `METRICS_ALLOWED_IPS`
2. **Token-based**: Set `METRICS_AUTH_TOKEN` and include `X-Metrics-Token` header
3. **Django auth**: Superusers can access metrics when logged in

Example:

```bash
# With token
curl -H "X-Metrics-Token: your-secret-token" http://localhost:8000/metrics/

# From allowed IP
curl http://localhost:8000/metrics/
```

### Health Check Endpoints

- `/metrics/health/` - Comprehensive health check with subsystem status
- `/metrics/readiness/` - Kubernetes readiness probe
- `/metrics/liveness/` - Kubernetes liveness probe

### Custom Metrics

Use the provided collectors to track custom metrics:

```python
from metrics.collectors import (
    track_custom_metric,
    track_user_activity,
    custom_metric_counter,
    custom_metric_gauge
)

# Track user activity
track_user_activity('registration')
track_user_activity('login', method='oauth')

# Track custom business metrics
track_custom_metric('payment', 'processed', value=1, gauge_value=99.99)

# Direct metric manipulation
custom_metric_counter.labels(type='order', action='created').inc()
custom_metric_gauge.labels(type='inventory').set(150)
```

### Celery Task Metrics

If using Celery, track task metrics:

```python
from metrics.collectors import celery_tasks_total, celery_task_duration_seconds
import time

# In your task
start_time = time.time()
try:
    # Task logic here
    celery_tasks_total.labels(task='send_email', status='success').inc()
except Exception as e:
    celery_tasks_total.labels(task='send_email', status='failure').inc()
    raise
finally:
    duration = time.time() - start_time
    celery_task_duration_seconds.labels(task='send_email').observe(duration)
```

## Available Metrics

### HTTP Metrics

- `django_http_requests_total` - Total HTTP requests by method, view, and status
- `django_http_request_duration_seconds` - Request latency histogram
- `django_http_requests_in_progress` - Currently processing requests
- `django_http_request_size_bytes` - Request size histogram
- `django_http_response_size_bytes` - Response size histogram

### Database Metrics

- `django_db_connections_total` - Active database connections
- `django_db_queries_total` - Query count by operation type
- `django_db_query_duration_seconds` - Query execution time

### Cache Metrics

- `django_cache_hits_total` - Cache hit count
- `django_cache_misses_total` - Cache miss count
- `django_cache_sets_total` - Cache set operations
- `django_cache_deletes_total` - Cache delete operations

### System Metrics

- `django_process_memory_bytes` - Process memory usage
- `django_process_cpu_percent` - Process CPU usage
- `django_process_threads_total` - Thread count
- `django_process_open_files_total` - Open file descriptors
- `django_python_gc_collections_total` - Garbage collection stats

### Business Metrics

- `django_user_registrations_total` - User registration count
- `django_user_logins_total` - User login count by method
- `django_active_users_total` - Active user gauge
- `django_custom_metric_total` - Custom counter
- `django_custom_metric_current` - Custom gauge

## Management Commands

### Export Metrics

```bash
# Print metrics to stdout
python manage.py export_metrics --print

# Push to Prometheus Pushgateway
python manage.py export_metrics --pushgateway localhost:9091 --job django_app
```

### Clean Up Old Metrics

```bash
# Clean up metrics older than 7 days
python manage.py cleanup_metrics

# Custom retention period
python manage.py cleanup_metrics --days 30

# Dry run
python manage.py cleanup_metrics --dry-run
```

## Prometheus Configuration

Add to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: "django_app"
    static_configs:
      - targets: ["localhost:8000"]
    metrics_path: "/metrics/"
    # If using token authentication
    authorization:
      credentials: "your-secret-token"
      type: "Bearer"
```

## Grafana Dashboards

Import these dashboard IDs for Django monitoring:

- Django Overview: 9528
- Django Request Metrics: 10288

Or create custom dashboards with queries like:

```promql
# Request rate
rate(django_http_requests_total[5m])

# Average response time
rate(django_http_request_duration_seconds_sum[5m]) / rate(django_http_request_duration_seconds_count[5m])

# Error rate
rate(django_http_requests_total{status=~"5.."}[5m])

# Memory usage
django_process_memory_bytes
```

## Performance Considerations

1. **Multiprocess Mode**: When using Gunicorn/uWSGI with multiple workers, set `PROMETHEUS_MULTIPROC_DIR`
2. **High Cardinality**: Avoid labels with many unique values (e.g., user IDs)
3. **Metric Storage**: The database storage is optional and mainly for debugging
4. **Middleware Order**: Ensure metrics middleware is properly positioned

## Security

1. Always use authentication for the metrics endpoint
2. Use HTTPS in production
3. Rotate `METRICS_AUTH_TOKEN` regularly
4. Limit `METRICS_ALLOWED_IPS` to known Prometheus servers
5. Consider network-level restrictions (firewall/security groups)

## Troubleshooting

### No metrics appearing

- Check `METRICS_ENABLED=True`
- Verify middleware is installed
- Check for import errors in logs

### High memory usage

- Reduce histogram buckets
- Check for high-cardinality labels
- Enable `PROMETHEUS_MULTIPROC_DIR` for multiprocess mode

### Authentication issues

- Verify IP is in `METRICS_ALLOWED_IPS`
- Check `X-Metrics-Token` header matches `METRICS_AUTH_TOKEN`
- Ensure superuser is logged in for Django auth

## Extending the Module

To add custom collectors:

1. Create new metrics in `collectors.py`
2. Add collection logic to your views/models
3. Update middleware if needed
4. Document the new metrics

Example:

```python
# In collectors.py
order_total = Histogram(
    'django_order_total_amount',
    'Order total amount in dollars',
    buckets=[10, 50, 100, 500, 1000, 5000]
)

# In your view/model
from metrics.collectors import order_total
order_total.observe(order.total_amount)
```
