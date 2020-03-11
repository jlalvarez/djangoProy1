from django import forms
from .models import Usuario

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

class SingupForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    
    OCCUPATION_CHOICES = [
        ('1', 'CathedralProfessor'),
        ('2', 'ResearchProfessor'),
        ('3', 'InstitutionalDirective'),
    ]
    Opciones = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OCCUPATION_CHOICES)
    