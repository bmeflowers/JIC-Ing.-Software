from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import EstudianteProfile, EmpresaProfile

class EstudianteRegisterForm(UserCreationForm):
    carrera = forms.CharField(max_length=100)
    semestre = forms.IntegerField()
    habilidades = forms.CharField(widget=forms.Textarea, required=False)
    cv = forms.FileField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EmpresaRegisterForm(UserCreationForm):
    nombre_empresa = forms.CharField(max_length=100)
    rubro = forms.CharField(max_length=100)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)
    sitio_web = forms.URLField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']