# mi_aplicacion/urls.py
from django.urls import path
from .views import medicalprocess

urlpatterns = [
    path('', medicalprocess().login, name='baselogin'),
    path('contact/', medicalprocess().contact, name='contact'),
]
