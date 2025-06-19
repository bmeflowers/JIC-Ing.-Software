from django.db import models
from django.contrib.auth.models import User
from vacantes.models import Vacante

# Create your models here.

class Postulacion(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postulaciones')
    vacante = models.ForeignKey(Vacante, on_delete=models.CASCADE, related_name='postulaciones')
    fecha_postulacion = models.DateTimeField(auto_now_add=True)

    nombre_completo = models.CharField("Nombre completo", max_length=150)
    edad = models.PositiveIntegerField("Edad")
    institucion = models.CharField("Institución educativa", max_length=150)
    motivo = models.TextField("¿Por qué deseas aplicar?", blank=True)
    cv = models.FileField("Currículum Vitae (PDF)", upload_to='postulaciones/cvs/', blank=True, null=True)

    class Meta:
        verbose_name = "Postulación"
        verbose_name_plural = "Postulaciones"
        ordering = ['-fecha_postulacion']
        unique_together = ('estudiante', 'vacante')  # evita postularse dos veces

    def __str__(self):
        return f"{self.estudiante.username} - {self.vacante.titulo}"