from django.shortcuts import render,redirect


from django.contrib.auth import authenticate, login

from django.contrib import messages
# Create your views here.


from django.shortcuts import render

class medicalprocess:
    def login(self,request):
        if request.method == 'POST':
    
            self.username = request.POST.get('username')

            self.password = request.POST.get('password')

            print(self.username,self.password)

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