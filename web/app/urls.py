from django.contrib import admin
from django.http import HttpResponse, JsonResponse
from django.urls import include, path
from rest_framework import status
from spectacular import urls as spectacular_urls


def healthcheck(request):
    return HttpResponse("OK")


def forbidden_error(request, *args, **kwargs):
    data = {
        "status_code": 403,
        "detail": "You do not have permission to perform this action.",
    }
    return JsonResponse(data, status=status.HTTP_403_FORBIDDEN)


def not_found_error(request, *args, **kwargs):
    data = {"status_code": 404, "detail": "Not found."}
    return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)


handler400 = "rest_framework.exceptions.bad_request"
handler403 = "app.urls.forbidden_error"
handler404 = "app.urls.not_found_error"
handler500 = "rest_framework.exceptions.server_error"

urlpatterns = [
    path("api/healthcheck/", healthcheck),
    path("api/admin/", admin.site.urls),
    path("api/", include(spectacular_urls)),
]
