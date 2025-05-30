import time

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, generate_latest

from .collectors import collect_db_metrics, collect_system_metrics


def is_metrics_allowed(request):
    """
    Check if the request is allowed to access metrics.
    Customize this based on your security requirements.
    """
    # Option 1: Allow from specific IPs (for Prometheus server)
    allowed_ips = getattr(settings, "METRICS_ALLOWED_IPS", ["127.0.0.1"])
    if request.META.get("REMOTE_ADDR") in allowed_ips:
        return True

    # Option 2: Check for a secret token in headers
    token = request.META.get("HTTP_X_METRICS_TOKEN")
    expected_token = getattr(settings, "METRICS_AUTH_TOKEN", None)
    if expected_token and token == expected_token:
        return True

    # Option 3: Allow authenticated superusers
    if request.user.is_authenticated and request.user.is_superuser:
        return True

    return False


@never_cache
@csrf_exempt
def metrics_view(request):
    """
    Prometheus metrics endpoint.
    Returns metrics in Prometheus text format.
    """
    # Check authorization
    if not is_metrics_allowed(request):
        return HttpResponse("Unauthorized", status=401)

    # Collect latest metrics
    collect_system_metrics()
    collect_db_metrics()

    # Generate metrics output
    metrics_output = generate_latest(REGISTRY)

    return HttpResponse(metrics_output, content_type=CONTENT_TYPE_LATEST)


@never_cache
def health_check_view(request):
    """
    Health check endpoint for monitoring.
    Returns JSON with service status.
    """
    start_time = time.time()
    health_status = {"status": "healthy", "checks": {}}

    # Database check
    try:
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status["checks"]["database"] = {
            "status": "healthy",
            "response_time_ms": round((time.time() - start_time) * 1000, 2),
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e),
        }

    # Cache check
    cache_start = time.time()
    try:
        from django.core.cache import cache

        cache.set("health_check", "ok", 1)
        if cache.get("health_check") == "ok":
            health_status["checks"]["cache"] = {
                "status": "healthy",
                "response_time_ms": round((time.time() - cache_start) * 1000, 2),
            }
        else:
            raise Exception("Cache read/write failed")
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["checks"]["cache"] = {
            "status": "unhealthy",
            "error": str(e),
        }

    # Redis check (if using Celery)
    if hasattr(settings, "REDIS_HOST"):
        redis_start = time.time()
        try:
            import redis

            r = redis.Redis(
                host=settings.REDIS_HOST,
                port=getattr(settings, "REDIS_PORT", 6379),
                password=getattr(settings, "REDIS_PASSWORD", None),
                decode_responses=True,
            )
            r.ping()
            health_status["checks"]["redis"] = {
                "status": "healthy",
                "response_time_ms": round((time.time() - redis_start) * 1000, 2),
            }
        except Exception as e:
            health_status["status"] = "degraded"
            health_status["checks"]["redis"] = {
                "status": "unhealthy",
                "error": str(e),
            }

    # Overall response time
    health_status["response_time_ms"] = round((time.time() - start_time) * 1000, 2)

    # Store health check result (optional)
    if "metrics" in settings.INSTALLED_APPS:
        try:
            from .models import ServiceHealthCheck

            ServiceHealthCheck.objects.create(
                service_name="api",
                status=health_status["status"],
                response_time_ms=health_status["response_time_ms"],
                metadata=health_status["checks"],
            )
        except Exception:
            pass  # Don't fail health check if metrics storage fails

    # Return appropriate status code
    status_code = 200 if health_status["status"] == "healthy" else 503

    return JsonResponse(health_status, status=status_code)


@never_cache
def readiness_check_view(request):
    """
    Kubernetes readiness probe endpoint.
    Checks if the service is ready to receive traffic.
    """
    try:
        # Check database
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        # Check cache
        from django.core.cache import cache

        cache.get("readiness_check")

        return JsonResponse({"status": "ready"})
    except Exception as e:
        return JsonResponse({"status": "not ready", "error": str(e)}, status=503)


@never_cache
def liveness_check_view(request):
    """
    Kubernetes liveness probe endpoint.
    Simple check to see if the service is alive.
    """
    return JsonResponse({"status": "alive"})
