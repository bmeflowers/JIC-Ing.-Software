# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import EmpresaProfile

class EmpresaProfileForm(forms.ModelForm):
    class Meta:
        model = EmpresaProfile
        fields = ['nombre_empresa', 'rubro', 'descripcion', 'sitio_web', 'logo']

class EstudianteRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        help_text="Obligatorio. 150 caracteres o menos. Sólo letras, dígitos y @ /./+/-/._.",
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre'})
    )
    email = forms.EmailField(
        label="Correo",
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa la contraseña'})
    )

    carrera = forms.CharField(
        label="Carrera",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Carrera'})
    )
    semestre = forms.IntegerField(
        label="Semestre",
        widget=forms.NumberInput(attrs={'placeholder': 'Semestre'})
    )
    habilidades = forms.CharField(
        label="Habilidades",
        widget=forms.Textarea(attrs={'placeholder': 'Cuéntanos sobre tus habilidades. Entre 3 a 5 que quieras destacar.'}),
        required=False
    )
    cv = forms.FileField(
        label="Añadir CV",
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'carrera', 'semestre', 'habilidades', 'cv']


class EmpresaRegisterForm(UserCreationForm):
    # Campos de usuario que sobrescriben los de UserCreationForm para personalizarlos
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        help_text="Obligatorio. 150 caracteres o menos. Sólo letras, dígitos y @ /./+/-/._.",
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre'})
    )
    email = forms.EmailField(
        label="Correo",
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa la contraseña'})
    )

    # Campos específicos de la empresa, con labels y placeholders como en la imagen
    nombre_empresa = forms.CharField(
        label="Nombre de la empresa",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de la empresa'})
    )
    rubro = forms.CharField(
        label="Rubro",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Sector en el que se especializa'})
    )
    descripcion = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(attrs={'placeholder': 'Cuéntanos sobre la empresa. Cantidad de trabajadores, a que se dedica y como es.'}),
        required=False
    )
    sitio_web = forms.URLField(
        label="Sitio web",
        required=False,
        widget=forms.URLInput(attrs={'placeholder': 'https://www.ejemplo.com/pagina-principal'})
    )

    logo = forms.ImageField(label="Logo de la empresa", required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'nombre_empresa', 'rubro', 'descripcion', 'sitio_web', 'logo']