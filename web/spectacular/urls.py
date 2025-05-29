from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

urlpatterns = [
    path("", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]
