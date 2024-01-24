from django.shortcuts import render,redirect


from django.contrib.auth import authenticate, login

from django.contrib import messages
# Create your views here.

from django.http import JsonResponse


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
        
        correokey=db.collection('pacientes').document(key).collection("info_paciente").document("paciente").get().to_dict()["correo_cir"]
        #db.collection('pacientes').document(key).get().to_dict()["correo"]
        #print("urldoc",correokey)
        docs = db.collection('cirujanos').document(correokey).collection("pacientes").document(key)
        return docs.get().to_dict()

    def buscar_responsable_usuario(self,key):
        
        responsabledicc=db.collection('pacientes').document(key).collection("info_paciente").document("responsable")
        return responsabledicc.get().to_dict()
    
    def buscar_historico_usuario(self,key):
        
        historicodb = db.collection('pacientes').document(key).collection("historico")
        docs = historicodb.stream()

        for doc in docs:
            print(f"Document ID: {doc.id}")
            print("Data:", doc.to_dict())

        return docs#.get().to_dict()

    
    # BUSCARDORES DE USUARIOS

    def homecirujano(self, request):
        id_numer = request.GET.get('buscadorid')
        tipo_id = request.GET.get('opcionesid')

        correouser =request.session.get('correo')
        tipousercompleto=request.session.get('tipousercompleto')


        key_search=str(tipo_id)+'_'+str(id_numer)
        print("testt",key_search,correouser)
        
        try:
            resultadosdatosusuario=self.buscar_usuario_admin(key_search)
            resultadosresponsable=self.buscar_responsable_usuario(key_search)

            resultadoss = {**resultadosdatosusuario, **resultadosresponsable}           
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
        #print(self.buscar_historico_usuario(key_search))
        try:
            resultadosdatosusuario=self.buscar_usuario_admin(key_search)
            resultadosresponsable=self.buscar_responsable_usuario(key_search)

            resultadoss = {**resultadosdatosusuario, **resultadosresponsable}
            resultadoss['tipo_usuario_completo']=tipousercompleto
        except:
            resultadoss={'tipo_usuario_completo':"ENFERMERA/O"}

        
        return render(request, 'homeenfermera.html', resultadoss)

    
    def homeadministrador(self, request):

        id_numer = request.GET.get('buscadorid')
        tipo_id = request.GET.get('opcionesid')

        tipousercompleto=request.session.get('tipousercompleto')
        
        key_search=str(tipo_id)+'_'+str(id_numer)

        print(key_search,tipousercompleto)

        try:
            resultadosdatosusuario=self.buscar_usuario_admin(key_search)
            resultadosresponsable=self.buscar_responsable_usuario(key_search)

            resultadoss = {**resultadosdatosusuario, **resultadosresponsable}
            
            resultadoss['tipo_usuario_completo']=tipousercompleto
        except:
            resultadoss={'tipo_usuario_completo':"ADMINISTRADOR/A"}

        #print("resultados",resultadoss)
        return render(request, 'homeadministrador.html', resultadoss)


    def contactlogincirujano(self, request):
        return render(request, "contactlogincirujano.html")
    
    def contactloginenfermera(self, request):
        return render(request, "contactloginenfermera.html")
    
    def contactloginadministrador(self, request):
        return render(request, "contactloadministrador.html")

class ingresarinformacion:
    def __init__(self):
        # Creando una instancia de la ClaseInterna
        self.Home = Home()

    def ingresarcirujano(self,request):
        
        nombre = str(request.GET.get('nombre')).upper()
        apellido = str(request.GET.get('apellido')).upper()

        especialidad = str(request.GET.get('especialidad')).upper()
        ciudad = str(request.GET.get('ciudad')).upper()

        direccion = str(request.GET.get('direccion')).upper()
        consultorio = str(request.GET.get('consultorio')).upper()

        celular = str(request.GET.get('celular')).upper()
        correo = str(request.GET.get('correo')).upper()


        # Define la referencia del documento con la cédula como identificador
        #print(correo)
        if correo != "NONE":
                doc_ref = db.collection('cirujanoinfo').document(correo)

                # Agrega los datos al documento
                doc_ref.set({
                            'nombre':nombre,
                            'apellido':apellido,
                            "especialidad":especialidad,
                            'ciudad':ciudad,
                            'direccion':direccion,
                            'consultorio':consultorio,
                            'celular':celular,
                            'correo':correo
                            })
                messages.warning(
                request, 'Ingresado el cirujano {}'.format(nombre+" "+ apellido))
                return render(request, 'alert_nofile_ingreso.html')
        else:
            return render(request, 'ingresarcirujano.html')

    def ingresarpacientes(self,request):

        tipodoc=str(request.GET.get('opcionesid')).upper()
        estadopaciente= str(request.GET.get('opcionestado')).upper()

        numdoc=str(request.GET.get('numdoc')).upper()
        pais= str(request.GET.get('pais')).upper()

        nombre=str(request.GET.get('nombre')).upper()
        edad= str(request.GET.get('edad')).upper()
        
        
        apellido = str(request.GET.get('apellido')).upper()
        fechadenacimiento = request.GET.get('fechanacimiento')

        correopaciente = str(request.GET.get('correopaciente')).upper()
        lugarnacimiento = str(request.GET.get('lugarnacimiento')).upper()

        celularpaciente = str(request.GET.get('celularpaciente')).upper()
        ciudaddenacimiento = str(request.GET.get('ciudaddenacimiento')).upper()

        cirujano = str(request.GET.get('cirujano')).upper()
        correocirujano = str(request.GET.get('correocirujano')).upper()


        # Define la referencia del documento con la cédula como identificador
        #print(fechadenacimiento,nombre,apellido)
        

        # Responsable

        retipodoc=str(request.GET.get('reopcionesid')).upper()
        renumdoc=str(request.GET.get('renumdoc')).upper()

        renombre=str(request.GET.get('renombre')).upper()
        reapellido = str(request.GET.get('reapellido')).upper()

        recelular = str(request.GET.get('recelular')).upper()
        reparentesco = str(request.GET.get('reparentesco')).upper()

        reciudad = str(request.GET.get('reciudad')).upper()
        recorreo = str(request.GET.get('recorreo')).upper()




        if correocirujano != "NONE":
                
                # DATOS DE PACIENTES
                doc_ref = db.collection('pacientes').document(str(tipodoc)+"_"+str(numdoc)).collection("info_paciente").document("paciente")

                # Agrega los datos al documento
                doc_ref.set({'tipo_doc':tipodoc,
                            'num_id':numdoc,
                            'nombre':nombre,
                            'apellido':apellido,
                            'correo':correopaciente,
                            'cirujano':cirujano,
                            'correo_cir':correocirujano,
                            'estado':estadopaciente,
                            'pais':pais,
                            'ciudad_de_nacimiento':ciudaddenacimiento,
                            'edad':edad,
                            'fecha_nacimiento':fechadenacimiento,
                            'lugar_nacimiento':lugarnacimiento,
                            'celular':celularpaciente})
                
                # RESPONSABLE DE PACIENTE
                doc_responsable = db.collection('pacientes').document(str(tipodoc)+"_"+str(numdoc)).collection("info_paciente").document("responsable")

                # Agrega los datos al documento
                doc_responsable.set({'retipo_doc':retipodoc,
                            'renum_id':renumdoc,
                            'renombre':renombre,
                            'reapellido':reapellido,
                            'reparentesco':reparentesco,
                            'recelular':recelular,
                            'recorreo':reciudad,
                            'reciudad':recorreo})
                

                #PACIENTES A CIRUJANOS

                doc_ref_p_a_c= db.collection('cirujanos').document(correocirujano).collection("pacientes").document(str(tipodoc)+"_"+str(numdoc))
                
                doc_ref_p_a_c.set({'tipo_doc':tipodoc,
                 'num_id':numdoc,
                 'nombre':nombre,
                 'apellido':apellido,
                 'correo':correopaciente,
                 'cirujano':cirujano,
                 'correo_cir':correocirujano,
                 'estado':estadopaciente,
                 'pais':pais,
                 'edad':edad,
                 'fecha_nacimiento':fechadenacimiento,
                 'lugar_nacimiento':lugarnacimiento,
                 'celular':celularpaciente,
                 'celular_cirujano':db.collection('cirujanoinfo').document(correocirujano).get().to_dict()["celular"],
                 })
                
                
                messages.warning(
                request, 'Ingresado el paciente {}'.format(nombre+" "+ apellido))
                return render(request, 'alert_nofile_ingreso.html')
        else:
            return render(request, 'ingresarpacientes.html')
    
    def preingresarhistoriaclinica(self,request):

        id_numer = request.GET.get('buscadorid')
        tipo_id = request.GET.get('opcionesid')
        tipousercompleto=request.session.get('tipousercompleto')


        
        key_search=str(tipo_id)+'_'+str(id_numer)
        

        fechasignosvitales=request.GET.get('fechasignosvitales')
        horasignosvitales=request.GET.get('horasignosvitales')
        temperaturacorporal=str(request.GET.get('temperaturacorporal')).upper()
        fecuenciacardiaca=str(request.GET.get('fecuenciacardiaca')).upper()
        saturacion=str(request.GET.get('saturacion')).upper()
        presionarterial=str(request.GET.get('presionarterial')).upper()
        tipoobservacion=str(request.GET.get('tipoobservacion')).upper()
        observaciones=str(request.GET.get('observaciones')).upper()
        
       
        try:
            resultadosdatosusuario=self.Home.buscar_usuario_admin(key_search)
            resultadosresponsable=self.Home.buscar_responsable_usuario(key_search)

            resultadoss = {**resultadosdatosusuario, **resultadosresponsable}
            resultadoss['tipo_usuario_completo']=tipousercompleto

        except:
            
            resultadoss={'tipo_usuario_completo':"ENFERMERA/O"}
        
        if str(fechasignosvitales) != "None":

            key_searchn=request.session.get('key_search')

            doc_ref = db.collection('pacientes').document(key_searchn).collection("historico").document(str(fechasignosvitales))\
                .collection(str(horasignosvitales)).document("signosvitales")

                # Agrega los datos al documento
            doc_ref.set({'fecha':fechasignosvitales,
                         'hora':horasignosvitales,
                         'temperatura_corporal':temperaturacorporal,
                        'fecuencia_cardiaca':fecuenciacardiaca,
                        'saturacion':saturacion,
                        'presion_arterial':presionarterial,
                        })
            
            doc_refob = db.collection('pacientes').document(key_searchn).collection("historico").document(str(fechasignosvitales))\
                .collection(str(horasignosvitales)).document("observaciones")
            
            if observaciones!="":
                doc_refob.set({'tipo_observacion':tipoobservacion,
                            'observaciones':observaciones})


            messages.warning(
            request, 'Ingresado el historico del paciente {}'.format( key_searchn))
            return render(request, 'alert_nofile_historiaclinica.html')
        
        else:
            request.session['key_search'] =key_search
            return render(request,"ingresarhistoriaclinica.html",resultadoss)

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