# postulaciones/forms.py
from django import forms
from .models import Postulacion

class PostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ['nombre_completo', 'edad', 'institucion', 'motivo', 'cv']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'institucion': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cv': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
