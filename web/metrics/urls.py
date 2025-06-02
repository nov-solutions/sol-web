from django.urls import include, path

from .views import health_check_view, liveness_check_view, readiness_check_view

app_name = "metrics"

urlpatterns = [
    # django_prometheus metrics endpoint
    path("", include("django_prometheus.urls")),
    # Health check endpoints
    path("health/", health_check_view, name="health-check"),
    path("readiness/", readiness_check_view, name="readiness-check"),
    path("liveness/", liveness_check_view, name="liveness-check"),
]
