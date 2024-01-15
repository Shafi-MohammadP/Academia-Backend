from django.db import models
# Create your models here.


class AdminNotifications(models.Model):
    NOTIFICATION_TYPE = (
        ('register', 'register'),
        ('course', 'course'),
        ('video', 'video'),
    )
    name = models.CharField(max_length=100)
    is_opened = models.BooleanField(default=False)
    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPE, default='register')
    created_time = models.DateTimeField(auto_now_add=True)
    key = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
