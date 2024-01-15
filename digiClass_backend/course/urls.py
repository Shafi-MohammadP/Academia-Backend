from django.urls import path
from .views import *

urlpatterns = [
    path('courseAdding/<int:tutor_id>/', CourseAdding.as_view()),
    # path('createCourse/<int:pk>/', CreateCourse.as_view()),
    path('courseList/', CourseList.as_view()),
    path('courseDetailview/<int:pk>/', CourseDetailView.as_view()),
    path('updateCourse/<int:tutor_id>/<int:pk>/', updateCourse.as_view()),
    path('categoryList/', CategoryList.as_view())

]
