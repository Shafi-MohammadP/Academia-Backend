from django.urls import path
from .import views
urlpatterns = [
    path('profileEdit/<int:pk>/', views.StudentProfileEdit.as_view()),
    path('StudentProfileShow/<int:student_id>/',
         views.StudentProfileShow.as_view())
]
