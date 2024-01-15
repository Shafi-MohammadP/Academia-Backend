from django.shortcuts import render
from urllib.parse import quote
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
# import requests
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
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


class Common_signup(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        email = request.data['email']
        if CustomUser.objects.filter(email=email).exists():

            data = {"Text": "Email already existed", "status": 400}
            return Response(data=data)

        if serializer.is_valid():
            user = serializer.save()
            # print(user.pk, 'pkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            current_site = get_current_site(request)
            mail_subject = 'Activate Your Account'
            message = render_to_string('user/Account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': default_token_generator.make_token(user)
            })
            if email and '@' in email:
                send_mail(
                    mail_subject,
                    message,
                    'AcademiaLearning@gmail.com',
                    [email],
                    fail_silently=False,
                    html_message=message
                )
                return Response({
                    'Text': "We've sended a verification link to you email address",
                    'data': serializer.data,
                    'status': status.HTTP_200_OK
                })
            else:
                data = {
                    "Text": "Invalid Email Adress",
                    "data": serializer.errors,
                    "status": status.HTTP_400_BAD_REQUEST
                }
                return Response(data=data)
        else:
            data = {
                "Text": "Error Occured",
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            }
            return Response(data=data)


@api_view(['GET'])
def ActivateAccountView(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        # print(uid, "uidddddddddddddddddddddddddddddddddddddddddddd")
        user = CustomUser._default_manager.get(id=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    # print(uid, user.pk, token,
    #       "gptttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        if user.role == 'student':
            student_data = {'user': user.id}
            student_serializer = studentProfileSerializer(data=student_data)
            if student_serializer.is_valid():
                student_serializer.save()
                print("student creation")
            else:
                user.delete()
                print("studente deletion")
                return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif user.role == 'tutor':
            tutor_data = {'user': user.id}
            tutor_serializer = tutorProfileSerializer(data=tutor_data)
            if tutor_serializer.is_valid():
                tutor_serializer.save()
                print("tutor creaion")
            else:
                user.delete()
                print("tutor deleteion")
                return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        print(user, "user activated succesfulyy")
        message = "Congrats, You have been succesfully registered"
        redirect_url = 'http://localhost:5173/Login/' + \
            '?message=' + message + '?token' + token
    else:
        print("Something FAiledd")
        message = 'Invalid activation link'
        redirect_url = 'http://localhost:5173/Login/' + '?message=' + message

    return HttpResponseRedirect(redirect_url)


# class TutorSignUp(APIView):
#     def post(self, request):
#         serializer = SignUpSerializer(
#             data=request.data, context={'role': 'tutor'})

#         check = request.data['email']
#         if CustomUser.objects.filter(email=check).exists():
#             data = {
#                 "Text": "Email already exist",
#                 "status": 400
#             }
#             return Response(data=data)

#         if serializer.is_valid():
#             user_instance = serializer.save()
#             # Assuming 'user' is the field name in TutorProfile
#             tutor_data = {'user': user_instance.id}
#             tutor_serializer = tutorProfileSerializer(data=tutor_data)

#             if tutor_serializer.is_valid():
#                 tutor_serializer.save()
#                 data = {"Text": "Account Created Successfully", "status": 200}
#                 return Response(data=data)
#             else:
#                 # If TutorProfile creation fails, delete the associated CustomUser
#                 user_instance.delete()
#                 return Response(tutor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                    "Text": "Logined Successfully",
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
        serializer = studentProfileSerializer(student_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class tutorProfileView(APIView):
    def get(self, request, user_id):
        tutor_profile = get_object_or_404(TutorProfile, user=user_id)
        serializer = tutorProfileSerializer(tutor_profile)
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


# class Authentication(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         content = {'user': str(request.user), 'userid': str(request.user.id), 'email': str(
#             request.user.email), 'is_active': str(request.user.is_active)}
#         return Response(content)
#     print('chekked=========================================<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>')
