from django.db import models
from users.models import TutorProfile
# Create your models here.
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver


class CourseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    tutor_id = models.ForeignKey(TutorProfile, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.FileField(upload_to="course images/", blank=True, null=True)
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return self.course_name
