"""
ASGI config for newCrm project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from main.consumers import CallConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newCrm.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,
    # WebSocket handler
    "websocket": AuthMiddlewareStack(URLRouter([path('ws/calls/', CallConsumer.as_asgi())])),
})
