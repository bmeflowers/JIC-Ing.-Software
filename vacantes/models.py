from django.db import models
from users.models import EmpresaProfile

class Vacante(models.Model):
    empresa = models.ForeignKey(EmpresaProfile, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255, verbose_name="Puesto de vacante")
    descripcion = models.TextField(verbose_name="Descripción del puesto")
    requerimientos = models.TextField(verbose_name="Requisitos")
    ubicacion = models.CharField(max_length=100, verbose_name="Ubicación")
    duracion = models.CharField(
        max_length=50,
        verbose_name="Duración del puesto",
        help_text="Ej: 3-6 meses",
        default="Indefinido"
    )
    cantidad_vacantes = models.PositiveIntegerField(
        verbose_name="Cantidad de vacantes",
        default=1
    )
    fecha_publicada = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField(verbose_name="Fecha límite de la publicación")
    activo = models.BooleanField(
        default=True,
        verbose_name="Activar vacante",
        help_text="Las vacantes activas serán visibles para los candidatos"
    )

    class Meta:
        verbose_name = "Vacante"
        verbose_name_plural = "Vacantes"
        ordering = ['-fecha_publicada']

    def __str__(self):
        return f"{self.titulo} - {self.empresa.nombre_empresa}"