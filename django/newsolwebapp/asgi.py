import os

from channels.routing import ProtocolTypeRouter, URLRouter
from decouple import config

from django.core.asgi import get_asgi_application
from django.urls import re_path

SITE_NAME = config("SITE_NAME")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django." + SITE_NAME + ".settings")

django_asgi_application = get_asgi_application()

http_routes = [re_path(r"", django_asgi_application)]
websocket_routes = []

application = ProtocolTypeRouter(
    {
        "http": URLRouter(http_routes),
        "websocket": URLRouter(websocket_routes),
    }
)
