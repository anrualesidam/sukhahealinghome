from django.shortcuts import render

# Create your views here.


from django.shortcuts import render

class medicalprocess:
    def login(self,request):
        return render(request, 'baselogin.html')
    
    def contact(self, request):
        return render(request, "contact.html")