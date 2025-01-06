from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path(
        "swagger.json",  # This explicitly handles the JSON schema
        SpectacularAPIView.as_view(),
        name="schema-json",
    ),
    path(
        "swagger.yaml",  # This explicitly handles the YAML schema
        SpectacularAPIView.as_view(),
        name="schema-yaml",
    ),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema-json"),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema-json"),
        name="schema-redoc",
    ),
]
