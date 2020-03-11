from django.shortcuts import render

from .forms import SingupForm, SingupModelForm

# Create your views here.

def registrar(request):
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

    return render(request, "mostrarForm.html", contexto)    

def login(request):
    f = SingupForm(request.POST or None)
    return render(request, "login.html", {"f":f})   

def checkLogin(request):
    f = SingupForm(request.POST or None)
    #print(dir(f))
    print(f.data)
    print(f.data.getlist("Opciones"))
    contexto = {
        "mensaje" : "Recibido correctamente",
        "titulo" : "Ver datos",
    }
    return render(request, "verForm.html", contexto)  


def home(request):
    contexto = {
        
    }
    return render(request, "base.html", contexto)   
