from django.http import JsonResponse
from django.views.decorators.cache import never_cache


@never_cache
def health_check_view(request):
    """Simple health check endpoint."""
    return JsonResponse({"status": "healthy"})


@never_cache
def readiness_check_view(request):
    """Kubernetes readiness probe endpoint."""
    try:
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ready"})
    except Exception as e:
        return JsonResponse({"status": "not ready", "error": str(e)}, status=503)


@never_cache
def liveness_check_view(request):
    """Kubernetes liveness probe endpoint."""
    return JsonResponse({"status": "alive"})
