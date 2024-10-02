from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.middleware.csrf import get_token


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"csrftoken": get_token(request)})
