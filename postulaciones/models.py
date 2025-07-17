from django.db import models
from users.models import EstudianteProfile
from vacantes.models import Vacante

class Notificacion(models.Model):
    estudiante = models.ForeignKey(EstudianteProfile, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif: {self.estudiante.user.username} - {self.mensaje[:30]}"

class Postulacion(models.Model):
    STATUS_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada'),
        ('Entrevista', 'En Entrevista'),
    )

    estudiante = models.ForeignKey(EstudianteProfile, on_delete=models.CASCADE, related_name='postulaciones')
    vacante = models.ForeignKey(Vacante, on_delete=models.CASCADE, related_name='postulaciones')
    fecha_postulacion = models.DateTimeField(auto_now_add=True)

    nombre_completo = models.CharField("Nombre y apellido", max_length=150)
    edad = models.PositiveIntegerField("Edad")
    telefono_1 = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(default="ejemplo@email.com")
    institucion = models.CharField("Institución educativa", max_length=150)
    motivo = models.TextField("¿Por qué deseas aplicar?", blank=True)
    cv = models.FileField("Currículum Vitae (PDF)", upload_to='postulaciones/cvs/', blank=True, null=True)
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendiente')
    class Meta:
        verbose_name = "Postulación"
        verbose_name_plural = "Postulaciones"
        ordering = ['-fecha_postulacion']
        unique_together = ('estudiante', 'vacante')  # evita postularse dos veces

    def __str__(self):
        return f"{self.estudiante.user.username} - {self.vacante.titulo} ({self.status})"

