from django.urls import path

from .consumer import AdminNotifications


websocket_urlpatterns = [
    path('ws/adminnotification/', AdminNotifications.as_asgi())
]
