from django.db import models
from users.models import EmpresaProfile

# Create your models here.
class Vacante(models.Model):
    empresa = models.ForeignKey(EmpresaProfile, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    requerimientos = models.TextField()
    ubicacion = models.CharField(max_length=100)
    fecha_publicada = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Vacante"
        verbose_name_plural = "Vacantes"
        ordering = ['-fecha_publicada']

    def __str__(self):
        return self.empresa.nombre_empresa
