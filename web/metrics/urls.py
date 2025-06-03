from django.urls import path
from django_prometheus import exports

app_name = "metrics"

urlpatterns = [
    path("", exports.ExportToDjangoView, name="prometheus-django-metrics"),
]
