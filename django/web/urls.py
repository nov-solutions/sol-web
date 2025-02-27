from core import views
from spectacular import urls as spectacular_urls

from django.contrib import admin
from django.urls import include, path
from django.views.defaults import (
    bad_request,
    page_not_found,
    permission_denied,
    server_error,
)

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/healthcheck/", views.healthcheck),
    path("docs/", include(spectacular_urls)),
]

handler400 = bad_request
handler403 = permission_denied
handler404 = page_not_found
handler500 = server_error
