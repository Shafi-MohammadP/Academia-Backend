from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view()),
    path('googlelogin/', views.GooglLogin.as_view()),
    # Student
    path('student-sign-up/', views.StudentSignUp.as_view()),
    path('studentProfile/<int:user_id>/', views.studentProfileView.as_view(),
         name='studentProfileView'),
    # Tutor
    path('tutor-signup/', views.TutorSignUp.as_view()),
    path('tutorProfile/<int:user_id>/',
         views.tutorProfileView.as_view(), name='tutorProfile'),

    # Admin
    path('studentList/', views.studentListing.as_view()),
    path('tutorListing/', views.tutorListing.as_view(), name='tutorListing'),
    path('ppurl/', views.NewTutoraLisiting.as_view()),


]
