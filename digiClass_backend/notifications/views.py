from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import AdminNotifications
from .serializer import AdminNotificationSerializer
# Create your views here.


class CertificateDetails(ListAPIView):
    queryset = AdminNotifications.objects.all()
    serializer_class = AdminNotificationSerializer