from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import TutorProfile
from tutor.models import Certificate
from .models import Course, CourseCategory
from .serializer import CourseSerializer, CourseCategorySerializer, IndividualCourseSerializer
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
# Create your views here.


class CourseAdding(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            tutor_id = kwargs.get('tutor_id')
            print(tutor_id, "----------------------->>")
            certificate = Certificate.objects.get(tutor=tutor_id)

            if not certificate.is_approved:
                data = {
                    "message": "Wait for Admin approval of your certificate",
                    "status": status.HTTP_401_UNAUTHORIZED
                }
                return Response(data=data)
            else:
                tutor = TutorProfile.objects.get(pk=tutor_id)
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)
                    data = {
                        "message": "Course added successfully",
                        "status": status.HTTP_200_OK
                    }
                else:
                    data = {
                        "message": serializer.errors,
                        "status": status.HTTP_400_BAD_REQUEST
                    }
                return Response(data=data)

        except Certificate.DoesNotExist:
            data = {
                "message": "Certificate not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(data=data)
        except TutorProfile.DoesNotExist:
            data = {
                "message": "Tutor not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(data=data)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        serializer.save()


class CourseDetailView(RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = IndividualCourseSerializer


class CourseList(ListAPIView):
    queryset = Course.objects.filter(is_available=True)
    serializer_class = CourseSerializer


class updateCourse(RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = IndividualCourseSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            if not user.role == 'tutor':
                data = {
                    "message": "You are not authorized to Edit Course",
                    "status": status.HTTP_403_FORBIDDEN
                }
                return Response(data=data)
            tutor_id = self.kwargs.get('tutor_id')
            course_id = self.kwargs.get('pk')
            course_details = Course.objects.get(
                pk=course_id, tutor_id=tutor_id)
            serializer = self.get_serializer(
                instance=course_details, data=request.data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                data = {
                    "message": "Course Updated Successfully",
                    "status": status.HTTP_200_OK
                }
            else:
                data = {
                    "message": serializer.errors,
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            return Response(data=data)
        except Course.DoesNotExist:
            data = {
                "message": "Course not found",
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)

    def perform_update(self, serializer):
        serializer.save()


class CategoryList(ListAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
