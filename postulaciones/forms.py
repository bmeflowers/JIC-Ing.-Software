from django import forms
from .models import Postulacion

class PostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ['nombre_completo', 'edad', 'telefono_1', 'email', 'institucion', 'motivo', 'cv']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Juan Pérez'
            }),
            'edad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu edad (solo números)'
            }),
            'telefono_1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. +507 1234 5678'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@correo.com'
            }),
            'institucion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de tu institución educativa'
            }),
            'motivo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Cuéntanos brevemente por qué deseas postular a esta vacante...'
            }),
            'cv': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

class PostulacionStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ['status']
        labels = {
            'status': 'Estado de la Postulación',
        }
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
