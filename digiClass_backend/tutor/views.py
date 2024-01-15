from django.shortcuts import render
from rest_framework.views import APIView
from users.models import CustomUser, TutorProfile
from .models import Certificate
from .serializer import ApplicationFormSerializer, CertificateSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.serializer import tutorProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from course.models import Course
from course.serializer import IndividualCourseSerializer

# Create your views here.


class TutorProfileShow(APIView):

    def get(self, request, user_id):
        print(user_id, '-------------------------->>')
        try:
            tutorProfile = TutorProfile.objects.get(user=user_id)
        except TutorProfile.DoesNotExist:
            data = {
                "message": "Tutor not found",
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)

        serializer = tutorProfileSerializer(tutorProfile)
        extracted_id = serializer.data.get('id', None)
        data = {
            "data": extracted_id,
            "status": status.HTTP_200_OK
        }
        return Response(data=data)


class TeacherCertificate(RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationFormSerializer
    queryset = Certificate.objects.all()
    # def

    def retrieve(self, request, *args, **kwargs):
        tutor_id = kwargs.get('tutor_id')
        print(tutor_id, "------------------->>>")
        if not TutorProfile.objects.filter(pk=tutor_id).exists():
            data = {
                "message": "Tutor not found",
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)
        try:
            certificate_instance = Certificate.objects.get(tutor=tutor_id)
            serializer = self.get_serializer(certificate_instance)
            data = {
                "data": serializer.data,
                "status": status.HTTP_200_OK
            }
            return Response(data=data)
        except Certificate.DoesNotExist:
            data = {
                "message": "Certificate not found",
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)

    def update(self, request, *args, **kwargs):
        tutor_id = kwargs.get('tutor_id')
        if not TutorProfile.objects.filter(pk=tutor_id).exists():
            data = {
                "message": "Tutor not found",
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)
        try:
            certificate_instance = Certificate.objects.get(tutor=tutor_id)
            serializer = self.get_serializer(
                certificate_instance, data=request.data, partial=True)
            if serializer.is_valid():
                tutor_instance = serializer.save()
                tutor_instance.tutor.is_certificate = True
                tutor_instance.tutor.save()
                data = {
                    "message": "Certificate updated successfully",
                    "status": status.HTTP_200_OK
                }
                return Response(data=data)
        except Certificate.DoesNotExist:
            data = {
                "message": "Certificate not found",
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)


class TeacherFormSubmission(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        tutor_id = kwargs.get('tutor_id')
        if not TutorProfile.objects.filter(pk=tutor_id).exists():
            data = {
                "message": "Tutor not found",
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)

        if Certificate.objects.filter(tutor=tutor_id).exists():
            data = {
                "message": "Already Submitted",
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data)
        serializer = ApplicationFormSerializer(data=request.data)

        if serializer.is_valid():
            teacher_form_instance = serializer.save()
            teacher_form_instance.tutor.is_certificate = True
            teacher_form_instance.tutor.save()

            data = {
                "message": "Application Submitted Successfully",
                "status": status.HTTP_200_OK
            }
            return Response(data=data)
        else:
            data = {
                "message": serializer.errors,
                "status": 400
            }
            return Response(data=data)


class CertificateView(APIView):
    def get(self, request, tutor_id):
        try:
            certificate = Certificate.objects.get(tutor=tutor_id)
            serializer = CertificateSerializer(certificate)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Certificate Not Found", "status": status.HTTP_404_NOT_FOUND})


class TutorProfileEdit(APIView):
    def patch(self, request, *args, **kwargs):
        tutor_id = kwargs.get('pk')

        try:
            tutor = TutorProfile.objects.get(pk=tutor_id)
        except:
            return Response({"message": "Teacher Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = tutorProfileSerializer(
            instance=tutor, data=request.data, partial=False)

        if serializer.is_valid():
            serializer.save()
            data = {
                "teacherData": serializer.data,
                "message": "Profile Updated Successfully",
            }

            return Response(data=data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TutorCoursesView(APIView):
    def get(self, request, *args, **kwargs):
        tutor_id = kwargs.get('pk')
        courses = Course.objects.filter(tutor_id=tutor_id, is_available=True)
        serializer = IndividualCourseSerializer(courses, many=True)
        if serializer:
            return Response(serializer.data)
        return Response({"message": "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # serializer_class = CourseSerializer

    # def get_queryset(self):
    #     # Assuming the tutor_id is passed as a query parameter in the URL
    #     tutor_id = self.request.query_params.get('pk')

    #     # You may need to adjust the filtering logic based on your model structure
    #     queryset = Course.objects.filter(tutor_id=tutor_id, is_available=False)
    #     print(queryset, "q--------------------------->>>>>>>>>>>>>>>>>")

    #     return queryset

    # def get_object(self):
    #     try:
    #         # Retrieve a specific course based on the primary key
    #         obj = Course.objects.filter(pk=self.kwargs['pk'])
    #         print(obj, "-----------------<<<<")
    #         self.check_object_permissions(self.request, obj)
    #         return obj
    #     except Course.DoesNotExist:
    #         content = {'detail': 'Not found.'}
    #         return Response(content, status=status.HTTP_404_NOT_FOUND)
