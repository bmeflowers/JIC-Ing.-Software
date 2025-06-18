from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EstudianteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    carrera = models.CharField(max_length=100)
    semestre = models.PositiveIntegerField()
    habilidades = models.TextField(blank=True)
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class EmpresaProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_empresa = models.CharField(max_length=100)
    rubro = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    sitio_web = models.URLField(blank=True)

    def __str__(self):
        return self.nombre_empresa

