from django.db import models
from django.contrib.auth.models import User

class Postulacion(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postulaciones')
    nombre_vacante = models.CharField(max_length=255)
    empresa = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ], default='pendiente')

    def __str__(self):
        return f"{self.estudiante.username} - {self.nombre_vacante} ({self.estado})"


