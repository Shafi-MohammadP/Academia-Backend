from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.serializer import CustomUserSerializer, tutorProfileSerializer
from .models import Course, CourseCategory


class CourseSerializer(ModelSerializer):
    tutor_profile = tutorProfileSerializer(source='tutor_id', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class IndividualCourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseCategorySerializer(ModelSerializer):

    class Meta:
        model = CourseCategory
        fields = "__all__"


# class CourseViewWithCategory(ModelSerializer):
