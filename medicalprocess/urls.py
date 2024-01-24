# mi_aplicacion/urls.py
from django.urls import path
from .views import medicalprocess,Home,ingresarinformacion

urlpatterns = [
    path('', medicalprocess().login, name='baselogin'),
    path('contact/', medicalprocess().contact, name='contact'),
    path('homecirujano/', Home().homecirujano, name='homecirujano'),
    path('homeadministrador/', Home().homeadministrador, name='homeadministrador'),
    path('homeenfermera/', Home().homeenfermera, name='homeenfermera'),
    path('contactlogincirujano/', Home().contactlogincirujano, name='contactlogincorujano'),
    path('contactloginenfermera/', Home().contactloginenfermera, name='contactloginenfermera'),
    path('contactloginandminstrador/', Home().contactloginadministrador, name='contactloginandminstrador'),
    path('ingresarcirujano/', ingresarinformacion().ingresarcirujano, name='ingresarcirujano'),
    path('ingresarpacientes/', ingresarinformacion().ingresarpacientes, name='ingresarpacientes'),
    path('ingresarhistoriaclinica/', ingresarinformacion().ingresarhistoriaclinica, name='ingresarhistoriaclinica'),
    #path('search/', SearchCirujano().search_pacientes, name='search'),
    
]
