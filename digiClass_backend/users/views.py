from django.shortcuts import render
from urllib.parse import quote
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
# import requests
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter
# from connectin.settings import STATIC_URL
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
# from .serializers import User_Sign_Up, myTokenObtainPairSerializer
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from rest_framework.generics import GenericAPIView, ListAPIView
from django.http import HttpResponseRedirect
from decouple import config
from .serializer import *
from .models import *
from rest_framework import status
from django.contrib.auth import authenticate
# Create your views here.


class StudentSignUp(APIView):
    def post(self, request):
        serializer = SignUpSerializer(
            data=request.data, context={'role': 'student'})

        check = request.data['email']
        if CustomUser.objects.filter(email=check).exists():
            data = {"Text": "Email already existed", "status": 400}
            return Response(data=data)

        if serializer.is_valid():
            user_instance = serializer.save()
            # Assuming 'user' is the field name in StudentProfile
            student_data = {'user': user_instance.id}
            print(student_data, 'student data-------------------------------->>>')
            student_serializer = studentProfileSerializer(data=student_data)

            if student_serializer.is_valid():
                student_serializer.save()
                data = {"Text": "Account Created Successfully", "status": 200}
                return Response(data=data)
            else:
                # If StudentProfile creation fails, delete the associated CustomUser
                user_instance.delete()
                return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TutorSignUp(APIView):
    def post(self, request):
        serializer = SignUpSerializer(
            data=request.data, context={'role': 'tutor'})

        check = request.data['email']
        if CustomUser.objects.filter(email=check).exists():
            data = {
                "Text": "Email already exist",
                "status": 400
            }
            return Response(data=data)

        if serializer.is_valid():
            user_instance = serializer.save()
            # Assuming 'user' is the field name in TutorProfile
            tutor_data = {'user': user_instance.id}
            tutor_serializer = tutorProfileSerializer(data=tutor_data)

            if tutor_serializer.is_valid():
                tutor_serializer.save()
                data = {"Text": "Account Created Successfully", "status": 200}
                return Response(data=data)
            else:
                # If TutorProfile creation fails, delete the associated CustomUser
                user_instance.delete()
                return Response(tutor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GooglLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get("username")
        password = request.data.get("password")
        print(email, username, password,
              '------------------------------------<<<<<<<<<<<<<<<<<<<<<<<<<<')

        existing_user = CustomUser.objects.filter(email=email).first()
        print(existing_user, "--------------------------------------------")
        # print(existing_user.role, "exisssssssssssssssssssssss")
        if existing_user:
            existing_user.is_google = True
            token = create_jwt_token(existing_user)
            data = {
                'status': 200,
                'token': token,
                'Text': "Logined Succesfully"
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        # Create an instance of the serializer with request data
        serializer = userGoogleSerializer(data=request.data)

        # Check if the data is valid before saving
        if serializer.is_valid():
            # Check if the user already exists
            user, created = CustomUser.objects.get_or_create(
                email=email, defaults={'username': username})

            if created:
                # If the user is created, set additional attributes and password
                user.is_active = True
                user.username = username
                user.is_google = True
                user.role = 'student'  # You might want to handle this based on your activation logic
                user.save()
                print(user.role, '-------------------------------------->>>>')

            # Authenticate the user
            # user = authenticate(request, email=email, password=password)

            if user is not None:
                # Generate a token for the user
                token = create_jwt_token(user)

                data = {
                    "Text": "Logined Succesfully",
                    'status': 200,
                    'token': token,
                    'user': serializer.data,

                }
                return Response(data=data, status=status.HTTP_201_CREATED)

        # If the serializer is not valid, return validation errors
        data = {
            "Text": serializer.errors,
            "status": 400
        }
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def create_jwt_token(user):
    refresh = RefreshToken.for_user(user)

    refresh['email'] = user.email
    refresh['id'] = user.id
    refresh['name'] = user.username
    refresh['role'] = user.role
    refresh['is_admin'] = user.is_superuser
    refresh['is_active'] = user.is_active
    refresh['is_google'] = user.is_google

    access_token = str(refresh.access_token)  # type: ignore
    refresh_token = str(refresh)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = myTokenObtainPairSerializer


class studentProfileView(APIView):
    def get(self, request, user_id):
        student_profile = get_object_or_404(StudentProfile, user=user_id)
        print(student_profile.bio)
        serializer = studentProfileSerializer(student_profile)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_4)


class tutorProfileView(APIView):
    def get(self, request, user_id):
        tutor_profile = get_object_or_404(TutorProfile, user=user_id)
        # print(tutor_profile.bio, '-------------------------------->>>>>>')
        serializer = tutorProfileSerializer(tutor_profile)
        # print(serializer.data, '00000000000000000000000000000-----<<<<<<<<<')
        return Response(serializer.data, status=status.HTTP_200_OK)


class studentListing(ListAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = studentProfileSerializer


class tutorListing(ListAPIView):
    queryset = TutorProfile.objects.all()
    serializer_class = tutorProfileSerializer


class NewTutoraLisiting(ListAPIView):
    queryset = TutorProfile.objects.all()
    serializer_class = tutorProfileSerializer
