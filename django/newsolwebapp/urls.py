from django.contrib import admin
from django.urls import include, path

from .urls_base import swagger_patterns

api_patterns = []

urlpatterns = [
    path("api/", include(api_patterns)),
    path("api/admin/", admin.site.urls),
    path("api/docs/", include(swagger_patterns)),
]
