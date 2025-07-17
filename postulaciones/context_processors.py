from .models import Notificacion

def notificaciones_estudiante(request):
    if request.user.is_authenticated and hasattr(request.user, 'estudianteprofile'):
        notificaciones = Notificacion.objects.filter(
            estudiante=request.user.estudianteprofile,
            leida=False
        ).order_by('-fecha')
        return {'notificaciones_bell': notificaciones}
    return {}
