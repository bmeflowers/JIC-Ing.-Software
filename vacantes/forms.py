from django import forms
from .models import Vacante

class VacanteRegisterForm(forms.ModelForm):
    class Meta:
        model = Vacante
        fields = ['titulo', 'descripcion', 'requerimientos', 'ubicacion', 'rango_salario', 'fecha_limite', 'activo']
        widgets = {
            'fecha_limite': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'titulo': 'Título de la Vacante',
            'descripcion': 'Descripción del Puesto',
            'requerimientos': 'Requisitos',
            'ubicacion': 'Ubicación',
            'rango_salario': 'Rango de Salario (Opcional)',
            'fecha_limite': 'Fecha límite de Aplicación',
            'activo': 'Vacante Activa'
        }