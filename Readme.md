# Introducción a Django

## Primeros Pasos

//TO DO
Instalar Python

//TO DO
Instalar pip 

//TO DO
- Instalar Django
```
python -m pip install django
```
```
WARNING: The script sqlformat.exe is installed in 'C:\Users\alvarez\AppData\Local\Packages\PythonSoftwareFoundation.Pyt  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location. 
```

- Podríamos crear un entorno virtual

```
# macOS/Linux
sudo apt-get install python3-venv    # If needed
python3 -m venv env

# Windows
python -m venv env
```

- Ver paquetes instalados con 
```
$ pip freeze
```

## Crear proyecto Django

```
$  django-admin startproject <nombre_proy>
```

## Iniciar proyecto
```
$ python manage.py runserver 0:8000
```
Acceder al proyecto: http://ip-maquina:8000

## Crear un usuario administrador

Aplicar las migraciones iniciales

```
$ python manage.py migrate
```

y crear un superusuario con

```
$ python manage.py createsuperuser
```
Acceder al administración:  http://ip-maquina:8000/admin



## Crear App.

Un proyecto puede tener varias App

```
$ python manage.py startapp <nombre_APP>
```

## Registrar la App en settings.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    ...
    'django.contrib.staticfiles',
    'nombre_APP',
]
```

## Crear un modelo

En el fichero models.py de la app deseada creamos una clase con atributos. Los
tipos de datos: https://docs.djangoproject.com/en/3.0/ref/models/fields/#field-types

```python
class Usuario(models.Model):
    nombre = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __str__(self):
        return self.nombre + " (" + self.email + ")."
    
    
```

## Migraciones 

Aplicar las migraciones con:

```
$ python manage.py makemigrations

$ python manage.py migrate
```


## Utilizar la consola iteractiva

```
$ python manage.py shell
```

Importar modelo a la consola : from boletin.models import Usuario   

Obtener listado de objetos del modelo: 

```python
usuarios = Usuario.objects.all()
```

Crear objetos:  
```python
u1 = Usuario.objects.create(nombre='Pepe',email='pepe@mail.com')   
```


## Registrar un modelo

En el fichero admin.py: importamos el modelo y lo registramos

```python
from .models import Usuario

admin.site.register(Usuario)
```


### Personalizar la interfaz

```python
class AdminUsuario(admin.ModelAdmin):
    list_display = ["__str__", "nombre", "emai", "timestamp"]
    list_filter = ["timestamp"]
    list_editable = ["email"]
    search_fields = ["nombre", "email"]
    class Meta:
        model = Usuario


admin.site.register(Usuario, AdminUsuario)
```


## Crear una vista

En el fichero views.py incluir:

```python
def vista1(request):
    contexto = {} # Incluir datos para pasar a la vista
    return render(request, "vista1.html", contexto)
```

## Crear template
En el fiichero nombre_proy/settings.py se incluyen las rutas a los templates en la sección DIRS

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Para crear una ruta usamos: os.path.join(BASE_DIR, ...)

Por ejemplo, incluimos:

```python
TEMPLATES = [
    {
    ...
        'DIRS': [os.path.join(BASE_DIR, "templates")],
    ...
]
```

En la ruta será necesario crear las vistas
 ../templates/vista1.html


## Asociar una URL a una acción

En el fichero nombre_proy/urls.py añadir a urlpatterns una línea path:

```python
from app1 import views

urlpatterns = [
    ...
    path('url/', views.vista1, name='nombre'),
    ...
]
```

En este caso, la petición http://host:8000/url ejecutaría el método vista1 del
fichero views.py.
Se podría utilizar la ruta creada con {% url 'nombre' %}


## Crear Formularios
https://docs.djangoproject.com/en/3.0/topics/forms/

En la app crear un fichero form.py y añadir:

```python
from django import forms

class miForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    
    OCCUPATION_CHOICES = [
        ('1', 'CathedralProfessor'),
        ('2', 'ResearchProfessor'),
        ('3', 'InstitutionalDirective'),
    ]
    Opciones = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OCCUPATION_CHOICES)
```


### Añadir una vista para mostrar el formulario

En views.py, importar el formulario e incluir en la acción correspodiente:

```python
from .forms import miForm

def nombre(request):
    form = miForm()
    contexto = {
        "form": form,
    }
    return render(request, "vista.html", contexto)
```

En una vista, se renderiza el formulario con {{ }}, por ejemplo, vista.html quedaría:

```html
<h1>Alta usuario</h1>

<form method="POST" action="{% url 'verForm' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Registrar" />
</form>
```

## Crear una vista para recbir los datos del formulario

En el fichero nombre_proy/urls.py, añadir una nueva ruta para la nueva vista:

```python
...

urlpatterns = [
    ...
    path('verForm', views.vista, name='verForm')
    ...
]
...
```

En el fichero views.py, incluir una nueva acción con:

```python
def vista(request):
    f = miForm(request.POST or None)
    # Procesar el formulario
    #print(dir(f))
    #print(f.data)
    #print(f.data.getlist('Opciones'))
    # componer contexto deseado
    contexto {
        'mensaje' : "Formulario recibido correctamente"
    }
    
    return render(request, "vista.html", contexto)  
```

La nueva vista (vista.html) quedaría:

```html
{% extends "base.html" %}


{% block title %}Ver Datos{% endblock %}

{% block content %}

<h1>{{ titulo }}</h1>

<div class="alert alert-success alert-dismissible fade show" role="alert">
    {{ mensaje }}
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
</div>



{% endblock %}
```


## Crear un modelo para formulario

En el fichero form.py añadir el siguiente código

```python
from django import forms
from .models import Usuario

# Añadir este código
class SingupModelForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nombre", "email"]
# hasta aquí

class SingupForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
```    
Cambiar el contenido del fichero admin.py con el siguiente:

```python
from django.contrib import admin

# Register your models here.
from .forms import SingupModelForm
from .models import Usuario

class AdminUsuario(admin.ModelAdmin):
    list_display = ["__str__", "nombre", "email", "timestamp"]
    form = SingupModelForm
    list_filter = ["timestamp"]
    list_editable = ["email"]
    search_fields = ["nombre", "email"]
    #class Meta:
    #    model = Usuario


admin.site.register(Usuario, AdminUsuario)
```

### Añadir validaciones al modelo del formulario

Para ello, crearemos métodos en la clase del modelo del formulaio:

```python
# Añadir los métodos siguientes en esta clase
class SingupModelForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nombre", "email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        base, proveedor = email.split("@")
        if not "uhu." in proveedor:
            raise forms.ValidationError("Utilice su correo institucional")
        return email
        
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        # validaciones
        return nombre
```

## Archivos estáticos

En settings debe existir en la sección INSTALLED_APPS la siguiente entrada:

```    
'django.contrib.staticfiles',
```

y la sección: STATIC_URL = '/static/'

Es necesario hacer una distinción de los ficheros estáticos en desarrollo y en producción.

Para ello, añadir para simular los ficheros estáticos en producción
y definir STATIC_ROOT con la ruta en la que se alojaran los ficheros.

```  
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_devel", "static"),
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_prod", "static")
```

Ahora crear los directorios 
- static_prod y dentro static
- static_devel y dentro static

STATIC_ROOT será la ruta de producción a la que serán enviados los ficheros
estáticos que se alojen en STATICFILES_DIRS

Ahora, en el fichero urls.py definir las rutas a los ficheros estáticos, con:

```python
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Para trasladar los ficheros desde el entorno de desarrollo al de producción 
```
$ python manage.py collectstatic
```


Para acceder a un fichero estático utiliza:

```
{% load static %}


<img src="{% static 'img/example.jpg' %}" alt="My image">

```


## Plantillas 

Sea el siguiente fichero base.html nuestra plantilla principal:

```html
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">

    <title>Hello, world!</title>
  </head>
  <body>
    
    <div class="container">
        


    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
  </body>
</html>
```

### Heredar de una plantilla base

En las vistas, incluir al principio la herencia de la plantilla principal:

```html
{% extends "base.html" %}
...

```

### Incluir un fichero en otro

En la plantilla base, podemos incluir el contenido de otros ficheros con include:

```html
...
  <body>
    
    <div class="container">
        
        {% include "navbar.html" %}

    </div>
...
```

Esto incluiría el contenido del fichero navbar.html, en la plantilla base.

### Añadir bloques (block) en la plantilla base

En una plantilla, se pueden crear bloques que se sustituirán con el contenido 
definido en el fichero que herada de esa plantilla.

```html
...
    <title>Proyecto1 | {% block title %}{% endblock %}</title>
...
  <body>
    
    <div class="container">
        
        {% include "navbar.html" %}
        
        {% block jumbotron %}
        {% endblock %}
         
        
        {% block content %}
        {% endblock %}

    </div>
...
```
Ahora, en el fichero que hereda la plantilla, se define el contenido que se incluirá
en el bloque de la plantilla base:

```html
{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block jumbotron %}
<!-- Aquí el contenido para el bloque jumbotron -->
<div class="jumbotron">
  <h1 class="display-4">Hello, world!</h1>
  <p class="lead">This is a simple hero unit, a simple jumbotron-style component for calling extra attention to featured content or information.</p>
  <hr class="my-4">
  <p>It uses utility classes for typography and spacing to space content out within the larger container.</p>
  <a class="btn btn-primary btn-lg" href="#" role="button">Learn more</a>
</div>
{% endblock %}


{% block content %}
<!-- Aquí el contenido para el bloque content -->
{% endblock %}

...
```

## Crispy Forms

De momento, ver:
- https://django-crispy-forms.readthedocs.io/en/latest/
- https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html


## Enlaces




... continuará ...

