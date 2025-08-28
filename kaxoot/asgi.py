import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaxoot.settings')

django_asgi_app = get_asgi_application()

from middlewere.jwt import JWTAuthMiddleware
from tests import routing as test_routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(test_routing.websocket_urlpatterns)
    ),
})
