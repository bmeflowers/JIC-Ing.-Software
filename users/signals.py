# users/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import EstudianteProfile, EmpresaProfile

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        # Verifica si se registró como estudiante o empresa desde el formulario
        if hasattr(instance, '_tipo_usuario') and instance._tipo_usuario == 'estudiante':
            EstudianteProfile.objects.create(user=instance)
        elif hasattr(instance, '_tipo_usuario') and instance._tipo_usuario == 'empresa':
            EmpresaProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    if hasattr(instance, 'estudianteprofile'):
        instance.estudianteprofile.save()
    elif hasattr(instance, 'empresaprofile'):
        instance.empresaprofile.save()
