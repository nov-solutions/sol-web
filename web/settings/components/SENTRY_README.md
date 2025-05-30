# Sentry Integration Module

This module provides comprehensive error tracking and performance monitoring using Sentry for Django applications.

## Features

- **Error Tracking**: Automatic exception capture with context
- **Performance Monitoring**: Transaction and span tracking
- **Celery Integration**: Task monitoring and error tracking
- **Redis Integration**: Redis command monitoring
- **Custom Filtering**: Ignore specific errors and URLs
- **Data Scrubbing**: Automatic removal of sensitive data
- **User Context**: Automatic user identification
- **Breadcrumbs**: Detailed event trail
- **Release Tracking**: Version-based error grouping

## Configuration

### Required Environment Variables

```bash
# Basic configuration
SENTRY_DSN=https://your-key@sentry.io/project-id
```

### Optional Environment Variables

```bash
# Environment and release
SENTRY_ENVIRONMENT=production  # Default: ENVIRONMENT value
SENTRY_RELEASE=v1.2.3  # Default: GIT_SHA or "unknown"

# Performance monitoring
SENTRY_TRACES_SAMPLE_RATE=0.1  # 10% of transactions (0.0-1.0)
SENTRY_PROFILES_SAMPLE_RATE=0.1  # 10% of transactions profiled

# Privacy and data handling
SENTRY_SEND_DEFAULT_PII=false  # Send personally identifiable information
SENTRY_SCRUB_IP_ADDRESS=false  # Anonymize IP addresses
SENTRY_REQUEST_BODIES=medium  # never, small, medium, always
SENTRY_WITH_LOCALS=true  # Include local variables in stack traces

# Debug and behavior
SENTRY_DEBUG=false  # Enable Sentry SDK debug mode
SENTRY_ATTACH_STACKTRACE=true  # Attach stack traces to messages
SENTRY_MAX_BREADCRUMBS=100  # Maximum breadcrumbs to store

# Control
SENTRY_FORCE_DISABLE=false  # Force disable Sentry
TEST_MODE=false  # Disable in test mode
```

## Usage

### Basic Error Capture

Errors are automatically captured by the Django and Celery integrations. For manual capture:

```python
from settings.components.sentry import (
    sentry_capture_exception,
    sentry_capture_message,
    sentry_add_breadcrumb,
    sentry_set_user_context
)

# Capture an exception
try:
    risky_operation()
except Exception as e:
    sentry_capture_exception(e)

# Capture a message
sentry_capture_message("Something important happened", level="warning")

# Add breadcrumbs for context
sentry_add_breadcrumb(
    message="User clicked checkout",
    category="user_action",
    level="info",
    data={"cart_total": 99.99}
)

# Set user context
sentry_set_user_context(request.user)
```

### Performance Monitoring

```python
from settings.components.sentry import (
    sentry_start_transaction,
    sentry_start_span
)

# Start a transaction
with sentry_start_transaction(name="process_order", op="task") as transaction:
    # Start a span within the transaction
    with sentry_start_span(op="db.query", description="fetch_user_orders"):
        orders = Order.objects.filter(user=user)

    with sentry_start_span(op="http.request", description="payment_gateway"):
        process_payment(order)
```

### Custom Context

```python
import sentry_sdk

# Set tags
with sentry_sdk.configure_scope() as scope:
    scope.set_tag("feature_flag", "new_checkout")
    scope.set_tag("plan", "premium")

# Set extra context
with sentry_sdk.configure_scope() as scope:
    scope.set_context("order_info", {
        "order_id": order.id,
        "total": order.total,
        "items": order.items.count()
    })
```

### Middleware Integration

Add the Sentry context middleware to automatically set user context:

```python
# In settings/components/base.py
MIDDLEWARE = [
    # ... other middleware
    'core.middleware.sentry.SentryContextMiddleware',
    # ... rest of middleware
]
```

## Filtering and Privacy

### Ignored Errors

The following errors are ignored by default:

- `django.security.DisallowedHost`
- `django.core.exceptions.PermissionDenied`
- `django.http.Http404`
- `rest_framework.exceptions.NotFound`
- `rest_framework.exceptions.PermissionDenied`
- `rest_framework.exceptions.NotAuthenticated`

### Ignored URLs

The following URL patterns are ignored:

- `/health/`
- `/healthcheck/`
- `/metrics/`
- `/readiness/`
- `/liveness/`

### Sensitive Data Scrubbing

The following fields are automatically scrubbed:

- `password`
- `secret`
- `token`
- `api_key`
- `access_token`
- `refresh_token`
- `private_key`
- `ssn`
- `credit_card`
- `cvv`
- `pin`

### Custom Filtering

The `before_send` function provides custom filtering:

- Filters test users (emails ending with @test.com)
- Additional URL pattern filtering
- Custom data scrubbing

## Celery Integration

Celery tasks are automatically monitored with:

- Task execution tracking
- Failure capture with context
- Retry monitoring
- Performance spans for tasks

## Performance Optimization

### Sampling Strategies

The module implements intelligent sampling:

- Fast, successful transactions: 10% sampling
- Slow or failed transactions: 100% sampling
- Configurable via `SENTRY_TRACES_SAMPLE_RATE`

### Reducing Overhead

To reduce Sentry overhead:

1. Lower `SENTRY_TRACES_SAMPLE_RATE` for high-traffic apps
2. Set `SENTRY_SEND_DEFAULT_PII=false`
3. Set `SENTRY_WITH_LOCALS=false` for production
4. Use `SENTRY_REQUEST_BODIES=small` or `never`

## Testing

### Disable in Tests

Sentry is automatically disabled when `TEST_MODE=true`.

### Test Error Capture

```python
# Force an error to test Sentry
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        # This will be captured by Sentry
        raise Exception("Test error for Sentry")
```

### Verify Configuration

```python
# Check if Sentry is configured
from django.conf import settings
import sentry_sdk

if hasattr(settings, 'sentry_configured') and settings.sentry_configured:
    print("Sentry is configured")
    print(f"DSN: {sentry_sdk.Hub.current.client.dsn}")
    print(f"Environment: {sentry_sdk.Hub.current.client.options['environment']}")
```

## Best Practices

1. **Use Breadcrumbs**: Add breadcrumbs for important user actions
2. **Set User Context**: Always set user context for authenticated requests
3. **Tag Appropriately**: Use tags for filtering (environment, feature flags, etc.)
4. **Meaningful Transactions**: Name transactions descriptively
5. **Handle PII Carefully**: Be mindful of `SENTRY_SEND_DEFAULT_PII`
6. **Monitor Performance**: Use transactions for critical paths
7. **Custom Context**: Add relevant context for debugging

## Troubleshooting

### Events Not Appearing

1. Check `SENTRY_DSN` is set correctly
2. Verify `SENTRY_FORCE_DISABLE=false`
3. Check `TEST_MODE=false`
4. Look for initialization errors in logs
5. Verify network connectivity to Sentry

### Performance Issues

1. Reduce `SENTRY_TRACES_SAMPLE_RATE`
2. Disable `SENTRY_WITH_LOCALS`
3. Set `SENTRY_REQUEST_BODIES=never`
4. Reduce `SENTRY_MAX_BREADCRUMBS`

### Missing Context

1. Ensure middleware is installed
2. Check user authentication
3. Verify breadcrumbs are being added
4. Check scope configuration

## Integration with Monitoring

Sentry complements other monitoring tools:

- Use with Prometheus metrics for complete observability
- Correlate errors with performance metrics
- Link deployment tracking with error rates

## Security Considerations

1. **DSN Security**: Keep `SENTRY_DSN` secret
2. **Data Scrubbing**: Review `SENTRY_SCRUB_FIELDS`
3. **PII Handling**: Consider `SENTRY_SEND_DEFAULT_PII` carefully
4. **IP Privacy**: Enable `SENTRY_SCRUB_IP_ADDRESS` if needed
5. **Local Variables**: Disable `SENTRY_WITH_LOCALS` in production if sensitive

## Removing the Module

If you don't need Sentry:

1. Set `SENTRY_FORCE_DISABLE=true` or remove `SENTRY_DSN`
2. Remove middleware from settings
3. Remove `sentry-sdk` from requirements.txt
4. Delete this settings file
