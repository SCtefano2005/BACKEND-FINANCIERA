# usuarios/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/notificaciones/', consumers.NotificacionConsumer.as_asgi()),
]
