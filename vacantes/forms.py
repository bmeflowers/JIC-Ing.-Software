from django import forms
from .models import Vacante

class VacanteRegisterForm(forms.ModelForm):
    fecha_limite = forms.DateField(
        input_formats=['%d/%m/%Y'],  # Este es el formato que Flatpickr usa
        widget=forms.DateInput(attrs={
            'type': 'text',
            'class': 'form-control datepicker',
            'placeholder': 'DD/MM/AAAA'
        })
    )

    class Meta:
        model = Vacante
        fields = [
            'titulo',
            'ubicacion',
            'duracion',
            'cantidad_vacantes',
            'fecha_limite',
            'descripcion',
            'requerimientos',
            'activo'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Ingeniero Agropecuario'
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Calle Principal #123, Ciudad'
            }),
            'duracion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 3-6 meses'
            }),
            'cantidad_vacantes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'fecha_limite': forms.DateInput(attrs={
            'type': 'text',  # importante para que Flatpickr no lo sobrescriba con el selector nativo
            'class': 'form-control datepicker',
            'placeholder': 'DD/MM/AAAA'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe las responsabilidades principales del puesto'
            }),
            'requerimientos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Especifica los requisitos (educación, experiencia, habilidades)'
            })
        }
        labels = {
            'titulo': 'Puesto de vacante',
            'ubicacion': 'Ubicación',
            'duracion': 'Duración del puesto',
            'cantidad_vacantes': 'Cantidad de vacantes',
            'fecha_limite': 'Fecha límite de la publicación',
            'descripcion': 'Descripción del puesto',
            'requerimientos': 'Requisitos',
            'activo': 'Activar vacante'
        }
        help_texts = {
            'activo': 'Las vacantes activas serán visibles para los candidatos'
        }