from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from postulaciones.models import Postulacion

# Create your views here.
@login_required
def dashboard_empresa(request):
    return render(request, 'dashboards/dashboard_empresa.html')

@login_required
def dashboard_estudiante(request):
    postulaciones = Postulacion.objects.filter(estudiante=request.user).order_by('-fecha_postulacion')
    return render(request, 'dashboards/dashboard_estudiante.html', {
        'postulaciones': postulaciones
    })
