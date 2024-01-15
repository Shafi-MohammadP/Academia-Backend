from rest_framework import serializers
from .models import AdminNotifications


class AdminNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminNotifications
        fields = "__all__"
