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