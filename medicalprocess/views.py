from django.shortcuts import render,redirect


from django.contrib.auth import authenticate, login

from django.contrib import messages
# Create your views here.


from django.shortcuts import render


import firebase_admin
from firebase_admin import credentials, firestore
import os
# Inicializar la aplicación con las credenciales descargadas

url = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "static/keys/sukha_doctor_history.json")
cred = credentials.Certificate(url)
firebase_admin.initialize_app(cred)
db = firestore.client()

class medicalprocess:
    def login(self,request):
        if request.method == 'POST':
    
            self.username = request.POST.get('username')

            self.password = request.POST.get('password')

            #print(self.username,self.password)

            user = authenticate(
                request, username=self.username.lower(), password=self.password)

            context = {'contenido': self.username.lower()}
            if user is not None:
                login(request, user)
                request.session['minitoring_username'] = self.username.lower()
                return render(request, 'home.html', context)
            else:
                # messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
                messages.warning(
                    request, 'Contraseña o nombre de usuario incorrecto, ¡compruébelo!')
                return render(request, 'alert_nofile.html')

        return render(request, 'login.html')
    
    def contact(self, request):
        return render(request, "contact.html")
    


class Home:
    def home(self, request):
        return render(request, "home.html")
    
    def contact(self, request):
        return render(request, "contactlogin.html")
 

class SearchCirujano:

    def search_pacientes(self,request):
        id_numer = request.GET.get('buscadorid')
        tipo_id = request.GET.get('opcionesid')
        
        key_search=str(tipo_id)+'_'+str(id_numer)
        print(key_search)
        def leer_documentos_coleccion(correo):
            docs = db.collection('cirujanos').document(correo).collection("pacientes").document(key_search)

            #print(docs.get().to_dict())
            return docs.get().to_dict()
        resultadoss=leer_documentos_coleccion('anderson.ruales@udea.edu.co')

        return render(request, 'home.html', resultadoss)