from django.shortcuts import render

from .forms import SingupForm, SingupModelForm

# Create your views here.

def vista1(request):
    titulo = "App1"
    if request.user.is_authenticated:
        titulo = "Bienvenido %s" %(request.user)
    form = SingupModelForm(request.POST or None)
    
    contexto = {
        "titulo": titulo,
        "form": form,
    }
    
    if form.is_valid():
        instance = form.save(commit=False)
        if not instance.nombre:
            instance.nombre = "noname"
        instance.save()
        print(instance)
        print(instance.timestamp)
        
        contexto = {
            "titulo": "Gracias %s" %(instance.nombre),
        }

    return render(request, "vista1.html", contexto)    

def home(request):
    contexto = {
        
    }
    return render(request, "base.html", contexto)   
