from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

from django.urls import path

spectacular_urls = [
    path("", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]
