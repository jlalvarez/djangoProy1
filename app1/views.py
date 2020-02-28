from django.shortcuts import render

from .forms import SingupForm

# Create your views here.

def vista1(request):
    form = SingupForm()
    contexto = {
        "form": form,
    }
    return render(request, "vista1.html", contexto)    
    
