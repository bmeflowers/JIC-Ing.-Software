from django.db import models
<<<<<<< HEAD
<<<<<<< Updated upstream

# Create your models here.
=======
from users.models import EstudianteProfile
from vacantes.models import Vacante

# Create your models here.

class Postulacion(models.Model):
    STATUS_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada'),
        ('Entrevista', 'En Entrevista'),
    )

    estudiante = models.ForeignKey(EstudianteProfile, on_delete=models.CASCADE, related_name='postulaciones')
=======
from django.contrib.auth.models import User
from vacantes.models import Vacante

# Create your models here.

class Postulacion(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postulaciones')
>>>>>>> bmeflowers_02
    vacante = models.ForeignKey(Vacante, on_delete=models.CASCADE, related_name='postulaciones')
    fecha_postulacion = models.DateTimeField(auto_now_add=True)

    nombre_completo = models.CharField("Nombre completo", max_length=150)
    edad = models.PositiveIntegerField("Edad")
    institucion = models.CharField("Institución educativa", max_length=150)
    motivo = models.TextField("¿Por qué deseas aplicar?", blank=True)
    cv = models.FileField("Currículum Vitae (PDF)", upload_to='postulaciones/cvs/', blank=True, null=True)
<<<<<<< HEAD
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendiente')
=======
>>>>>>> bmeflowers_02

    class Meta:
        verbose_name = "Postulación"
        verbose_name_plural = "Postulaciones"
        ordering = ['-fecha_postulacion']
        unique_together = ('estudiante', 'vacante')  # evita postularse dos veces

    def __str__(self):
<<<<<<< HEAD
        return f"{self.estudiante.user.username} - {self.vacante.titulo} ({self.status})"
    
>>>>>>> Stashed changes
=======
        return f"{self.estudiante.username} - {self.vacante.titulo}"
>>>>>>> bmeflowers_02
