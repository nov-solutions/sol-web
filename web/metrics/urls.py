from django.urls import path

from .views import (
    health_check_view,
    liveness_check_view,
    metrics_view,
    readiness_check_view,
)

app_name = "metrics"

urlpatterns = [
    # Prometheus metrics endpoint
    path("", metrics_view, name="prometheus-metrics"),
    # Health check endpoints
    path("health/", health_check_view, name="health-check"),
    path("readiness/", readiness_check_view, name="readiness-check"),
    path("liveness/", liveness_check_view, name="liveness-check"),
]
