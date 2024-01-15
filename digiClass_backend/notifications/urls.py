from django.urls import path
from .import views
urlpatterns = [
    path('demoView/',views.CertificateDetails.as_view())
]
