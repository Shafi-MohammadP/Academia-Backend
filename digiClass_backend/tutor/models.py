from django.db import models
from users.models import CustomUser, TutorProfile
from phonenumber_field.modelfields import PhoneNumberField
from notifications.models import AdminNotifications
# Create your models here.


class Certificate(models.Model):
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE)
    certificate = models.FileField(
        upload_to='teacher_certificates/', blank=True, null=True)
    is_approved = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        if self.tutor:
            return self.tutor.user.username

# class TeacherCertificate(models.Model):
#     user = models.ForeignKey(
#         TutorProfile, on_delete=models.CASCADE, null=True)
#     certificate = models.FileField(
#         upload_to='teacher_certificates/', blank=True, null=True)
#     is_approved = models.BooleanField(default=False, null=True, blank=True)

#     def save(self, *args, **kwargs):
#         created = not self.pk
#         super(TeacherCertificate, self).save(*args, **kwargs)

#         if created:

#             notification = AdminNotifications(
#                 name=f"New  Teacher Registered: {self.user.user.username}",
#                 is_opened=False,
#                 notification_type='register',
#                 key=self.id
#             )
#             print("working here-------------------->>>>")

#             notification.save()

#     def __str__(self):
#         if self.user:
#             return self.user.user.username
