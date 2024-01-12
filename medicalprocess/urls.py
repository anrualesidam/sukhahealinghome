# mi_aplicacion/urls.py
from django.urls import path
from .views import medicalprocess,Home

urlpatterns = [
    path('', medicalprocess().login, name='baselogin'),
    path('contact/', medicalprocess().contact, name='contact'),
    path('home/', Home().home, name='home'),
    path('contactlogin/', Home().contact, name='contactlogin'),
    
]
