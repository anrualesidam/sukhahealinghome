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

            self.tipo_user = request.POST.get('opcionesid')

            tipos_de_usuarios={"MECI":"MÉDICO CIRUJANO","ENFER":"ENFERMERA/O","ADMIN":"ADMINISTRADOR/A"}

            #print(self.username,self.password,self.tipo_user)

            self.user = authenticate(
                request, username=self.username.lower(), password=self.password)

            context = {'contenido': self.username.lower(),'tipo_usuario_completo':tipos_de_usuarios[self.tipo_user]}
            

            if self.user is not None:

                if self.tipo_user == "":
                    messages.warning(
                    request, 'Seleccionar tipo de usuario')
                    return render(request, 'alert_nofile.html')
                
                elif self.tipo_user!= self.user.tipo_user:
                    messages.warning(
                    request, '{} no es tu tipo de usuario, ¡compruébelo!'.format(tipos_de_usuarios[self.tipo_user]))
                    return render(request, 'alert_nofile.html')
                
                login(request, self.user)

                if self.user.tipo_user=="MECI":
                    request.session['correo'] = self.username.lower()
                    request.session['tipouser'] =self.tipo_user
                    request.session['tipousercompleto'] = tipos_de_usuarios[self.tipo_user]
                    return render(request, 'homecirujano.html', context)

                elif self.user.tipo_user=="ENFER":
                    request.session['correo'] = self.username.lower()
                    request.session['tipouser'] =self.tipo_user
                    request.session['tipousercompleto'] = tipos_de_usuarios[self.tipo_user]
                    return render(request, 'homeenfermera.html', context)
                
                elif self.user.tipo_user=="ADMIN":
                    request.session['correo'] = self.username.lower()
                    request.session['tipouser'] =self.tipo_user
                    request.session['tipousercompleto'] = tipos_de_usuarios[self.tipo_user]
                    return render(request, 'homeadministrador.html', context)               

            else:
                # messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
                messages.warning(
                    request, 'Contraseña o nombre de usuario incorrecto, ¡compruébelo!')
                return render(request, 'alert_nofile.html')

        return render(request, 'login.html')
    
    def contact(self, request):
        return render(request, "contact.html")
    


class Home:

    def leer_documentos_coleccion(self,correo,key_search):
            docs = db.collection('cirujanos').document(correo).collection("pacientes").document(key_search)
            return docs.get().to_dict()
        
    def buscar_usuario_admin(self,key):
        correokey=db.collection('pacientes').document(key).get().to_dict()["correo"]
        print("urldoc",correokey)
        docs = db.collection('cirujanos').document(correokey).collection("pacientes").document(key)
        return docs.get().to_dict()

    
    # BUSCARDORES DE USUARIOS

    def homecirujano(self, request):
        id_numer = request.GET.get('buscadorid')
        tipo_id = request.GET.get('opcionesid')
        correouser =request.session.get('correo')
        tipousercompleto=request.session.get('tipousercompleto')


        key_search=str(tipo_id)+'_'+str(id_numer)
        print("testt",key_search,correouser)
        #try:
        
        try:
            resultadoss=self.leer_documentos_coleccion(correouser,key_search)
            resultadoss['tipo_usuario_completo']=tipousercompleto
        except:
            resultadoss={"tipo_usuario_completo":"MÉDICO CIRUJANO"}#['tipo_usuario_completo']="MÉDICO CIRUJANO"
            

        return render(request, 'homecirujano.html', resultadoss)

    
    def homeenfermera(self, request):

        id_numer = request.GET.get('buscadorid')
        tipo_id = request.GET.get('opcionesid')
        tipousercompleto=request.session.get('tipousercompleto')
        
        key_search=str(tipo_id)+'_'+str(id_numer)

        #print(key_search,tipousercompleto)

        try:
            resultadoss=self.buscar_usuario_admin(key_search)
            resultadoss['tipo_usuario_completo']=tipousercompleto
        except:
            resultadoss={'tipo_usuario_completo':"ENFERMERA/O"}

        
        return render(request, 'homeenfermera.html', resultadoss)

    
    def homeadministrador(self, request):

        id_numer = request.GET.get('buscadorid')
        tipo_id = request.GET.get('opcionesid')

        tipousercompleto=request.session.get('tipousercompleto')
        
        key_search=str(tipo_id)+'_'+str(id_numer)

        try:
            resultadoss=self.buscar_usuario_admin(key_search)
            resultadoss['tipo_usuario_completo']=tipousercompleto
        except:
            resultadoss={'tipo_usuario_completo':"ADMINISTRADOR/A"}
        return render(request, 'homeadministrador.html', resultadoss)


    def contact(self, request):
        return render(request, "contactlogin.html")
 
"""
class SearchCirujano:

    def search_pacientes(self,request):
        id_numer = request.GET.get('buscadorid')
        tipo_id = request.GET.get('opcionesid')

        correouser =request.session.get('correo')
        tipouser=request.session.get('tipouser')
        tipousercompleto=request.session.get('tipousercompleto')
        
        key_search=str(tipo_id)+'_'+str(id_numer)
        print(key_search,tipousercompleto)

        def leer_documentos_coleccion(correo):
            docs = db.collection('cirujanos').document(correo).collection("pacientes").document(key_search)
            return docs.get().to_dict()
        
        def buscar_usuario_admin(key):
            correokey=db.collection('pacientes').document(key).get().to_dict()["correo"]
            print("urldoc",correokey)


            docs = db.collection('cirujanos').document(correokey).collection("pacientes").document(key)
            return docs.get().to_dict()
        
        if tipouser=="MECI":
            resultadoss=leer_documentos_coleccion(correouser)
            resultadoss['tipo_usuario_completo']=tipousercompleto
            return render(request, 'homecirujano.html', resultadoss)
        
        elif  tipouser=="ENFER":
            resultadoss=buscar_usuario_admin(key_search)
            resultadoss['tipo_usuario_completo']=tipousercompleto
            return render(request, 'homeenfermera.html', resultadoss)
        
        elif tipouser=="ADMIN":
            #print("ADMIN")
            resultadoss=buscar_usuario_admin(key_search)
            resultadoss['tipo_usuario_completo']=tipousercompleto
            return render(request, 'homeadministrador.html', resultadoss)

        else:
            messages.warning(
            request, 'Ingresar Nuevamente')
            return render(request, 'alert_nofile.html')

        

        """