from django.shortcuts import render
from rest_framework.views import APIView
from users.models import StudentProfile
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status
from users.serializer import studentProfileSerializer
# Create your views


class StudentProfileEdit(APIView):

    def patch(self, request, *args, **kwargs):
        student_id = kwargs.get('pk')
        # print(student_id, "id----------------->>>>")
        # print(request.data, "------------------------------------------->>>>>")
        try:
            student = StudentProfile.objects.get(pk=student_id)
        except StudentProfile.DoesNotExist:
            return Response({"message": "Student Not Found", "status": status.HTTP_404_NOT_FOUND})

        # Update the student profile with the new data
        serializer = studentProfileSerializer(
            instance=student, data=request.data, partial=False)

        if serializer.is_valid():
            serializer.save()
            # print(serializer.data, "Mohammad")
            data = {
                "userData": serializer.data,
                "message": "Profile Updated Successfully",
                "status": status.HTTP_200_OK,


            }
            return Response(data=data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentProfileShow(APIView):
    def get(self, request, student_id):
        try:
            studentProfile = StudentProfile.objects.get(user=student_id)
        except StudentProfile.DoesNotExist:
            data = {
                "message": "Student not found",
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        serializer = studentProfileSerializer(studentProfile)
        extract_id = serializer.data.get('id', None)
        data = {
            "data": extract_id,
            "status": status.HTTP_200_OK
        }
        return Response(data=data, status=status.HTTP_200_OK)
