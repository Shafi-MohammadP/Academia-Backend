from django.urls import path

from .consumer import AdminNotifications, TutorNotification, StudentNotification


websocket_urlpatterns = [
    path('ws/adminnotification/', AdminNotifications.as_asgi()),
    path('ws/tutor_notifications/', TutorNotification.as_asgi()),
    path('ws/student_notifications/', StudentNotification.as_asgi()),
]
