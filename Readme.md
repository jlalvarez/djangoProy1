# Introducción a Django

## Primeros Pasos

//TO DO
Instalar Python

//TO DO
Instalar pip 

//TO DO
Instalar Django

Podríamos crear un entorno de desarrollo con VirtualEnv

Ver paquetes instalados con $ pip freeze

## Crear proyecto Django

```
$  django-admin startproject <nombre_proy>
```

## Iniciar proyecto
```
$ python manage.py runserver 0:8000
```
Acceder al proyecto: http://ip-maquina:8080

## Crear un usuario administrador

Aplicar las migraciones iniciales

```
$ python manage.py migrate
```

y crear un superusuario con

```
$ python manage.py createsuperuser
```
Acceder al administración:  http://ip-maquina:8080/admin



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

En el fichero nombre_proy/urls.py añadir:

```python
from app1 import views

urlpatterns = [
    ...
    path('', views.vista1, name='home')
]
```



## Crear Formularios
https://docs.djangoproject.com/en/3.0/topics/forms/

En la app crear un fichero form.py y añadir:

```python
from django import forms

class SingupForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
```


### Añadir a una vista

En views.py, importar el formulario e incluir en la acción correspodiente:

```python
from .forms import SingupForm

def inicio(request):
    form = SingupForm()
    contexto = {
        "form": form,
    }
    return render(request, "vista.html", contexto)
```

En la plantilla renderizar con {{ }}, por ejemplo el vista.html

```html
<h1>Alta usuario</h1>

<form method="POST" action="">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Registrar" />
</form>
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



... continuará ...