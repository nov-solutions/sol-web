from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie


def healthcheck(request):
    return HttpResponse("OK")


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"csrftoken": get_token(request)})
