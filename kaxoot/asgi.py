import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaxoot.settings')

# ⚡️ Django apps registry shu yerda ishga tushadi
django_asgi_app = get_asgi_application()

# ✅ Endi middleware va routingni import qilamiz
from middlewere.jwt import JWTAuthMiddleware
from tests import routing as test_routing   # sizning websocket routingi shu yerda bo‘lishi kerak

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(test_routing.websocket_urlpatterns)
    ),
})
