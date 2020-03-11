
from django.shortcuts import render


def about(request):
    contexto = {
        "titulo": "About"
    }
    return render(request, "about.html", contexto)    
