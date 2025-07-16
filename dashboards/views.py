from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from vacantes.models import Vacante
import random

@login_required
def dashboard_estudiante(request):
    vacantes = list(
        Vacante.objects.filter(activo=True)
        .order_by('-fecha_publicada')[:15]
        .select_related('empresa')
    )
    random.shuffle(vacantes)
    vacantes = vacantes[:3]
    return render(request, 'dashboards/dashboard_estudiante.html', {
        'vacantes': vacantes
    })

@login_required
def dashboard_empresa(request):
    return render(request, 'dashboards/dashboard_empresa.html')
