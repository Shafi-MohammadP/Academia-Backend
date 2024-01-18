from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone
from .models import *
from course.models import Course
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from notifications.models import Notifications
from users.models import CustomUser


channel_layer = get_channel_layer()


@receiver(post_save, sender=Course)
def send_course_created_notification(sender, instance, created, *args, **kwargs):

    if created:
        notification_text = f'New Course {instance.course_name} Created by {instance.tutor_id.user.username}'
        admin_user = CustomUser.objects.filter(is_superuser=True).first()
        Notifications.objects.create(
            user=admin_user, text=notification_text, course=instance)
        print(notification_text, "------------------------------>>>>>>")
        async_to_sync(channel_layer.group_send)(
            "admin_group",
            {
                'type': 'create_notification',
                'message': notification_text
            }
        )
