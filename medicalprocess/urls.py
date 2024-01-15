# mi_aplicacion/urls.py
from django.urls import path
from .views import medicalprocess,Home,SearchCirujano

urlpatterns = [
    path('', medicalprocess().login, name='baselogin'),
    path('contact/', medicalprocess().contact, name='contact'),
    path('homecirujano/', Home().homecirujano, name='homecirujano'),
    path('homeadministrador/', Home().homeadministrador, name='homeadministrador'),
    path('homeenfermera/', Home().homeenfermera, name='homeenfermera'),
    path('contactlogin/', Home().contact, name='contactlogin'),
    path('search/', SearchCirujano().search_pacientes, name='search'),
    
]
