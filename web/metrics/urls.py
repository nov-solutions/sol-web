from django.urls import include, path

app_name = "metrics"

urlpatterns = [
    path("metrics/", include("django_prometheus.urls")),
]
