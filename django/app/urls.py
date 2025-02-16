from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

from django.contrib import admin
from django.urls import path
from django.views.defaults import (
    bad_request,
    page_not_found,
    permission_denied,
    server_error,
)

from . import views

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/healthcheck/", views.healthcheck),
]

spectacular_urls = [
    path("docs/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]

urlpatterns += spectacular_urls

handler400 = bad_request
handler403 = permission_denied
handler404 = page_not_found
handler500 = server_error
