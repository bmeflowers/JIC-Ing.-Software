from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Postulacion
from vacantes.models import Vacante
from .forms import PostulacionForm
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.

@login_required
def postular_vacante(request, vacante_id):
    vacante = get_object_or_404(Vacante, id=vacante_id)
    
    # Verificar si el usuario ya está postulado antes de procesar el formulario
    postulacion_existente = Postulacion.objects.filter(
        estudiante=request.user,
        vacante=vacante
    ).exists()
    
    if postulacion_existente:
        messages.warning(request, '⚠️ Ya te has postulado a esta vacante anteriormente')
        return redirect('vacantes:vacante_publica_detalles', pk=vacante.id)
    
    if request.method == 'POST':
        form = PostulacionForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                postulacion = form.save(commit=False)
                postulacion.estudiante = request.user
                postulacion.vacante = vacante
                postulacion.save()
                
                messages.success(request, '✅ Postulación enviada correctamente')
                return redirect('ver_postulaciones')
                
            except IntegrityError:
                messages.error(request, '❌ Error: Ya tienes una postulación activa para esta vacante')
                return redirect('vacantes:vacante_publica_detalles', vacante_id=vacante.id)
    else:
        form = PostulacionForm()
    
    context = {
        'form': form,
        'vacante': vacante,
        'ya_postulado': postulacion_existente
    }
    return render(request, 'postulaciones/postular_form.html', context)

@login_required
def ver_postulaciones(request):
    postulaciones = Postulacion.objects.filter(
        estudiante=request.user
    ).select_related('vacante', 'vacante__empresa')
    
    return render(request, 'postulaciones/ver_postulaciones.html', {
        'postulaciones': postulaciones,
        'titulo': 'Mis Postulaciones'
    })