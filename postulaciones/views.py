from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Postulacion
from vacantes.models import Vacante
from .forms import PostulacionForm
from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView
from users.models import EmpresaProfile, EstudianteProfile
from .forms import PostulacionStatusUpdateForm

# Create your views here.

@login_required
def postular_vacante(request, vacante_id):
    try:
        estudiante_profile = request.user.estudianteprofile
    except EstudianteProfile.DoesNotExist:
        messages.error(request, '❌ Necesitas un perfil de estudiante para postularte.')
        return redirect('users:registroEst')

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Postulacion
from vacantes.models import Vacante
from .forms import PostulacionForm
from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView
from users.models import EmpresaProfile, EstudianteProfile
from .forms import PostulacionStatusUpdateForm

# Create your views here.

@login_required
def postular_vacante(request, vacante_id):
    try:
        estudiante_profile = request.user.estudianteprofile
    except EstudianteProfile.DoesNotExist:
        messages.error(request, '❌ Necesitas un perfil de estudiante para postularte.')
        return redirect('users:registroEst')
                        
    vacante = get_object_or_404(Vacante, id=vacante_id)
    
    # Verificar si el usuario ya está postulado antes de procesar el formulario
    postulacion_existente = Postulacion.objects.filter(
        estudiante=estudiante_profile,
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
                postulacion.estudiante = estudiante_profile
                postulacion.vacante = vacante
                postulacion.save()
                
                messages.success(request, '✅ Postulación enviada correctamente')
                return redirect('postulaciones:ver_postulaciones')

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
    try:
        estudiante_profile = request.user.estudianteprofile
    except EstudianteProfile.DoesNotExist:
        messages.error(request, '❌ Necesitas un perfil de estudiante para ver tus postulaciones.')
        return redirect('users:registroEst')
    
    postulaciones = Postulacion.objects.filter(
        estudiante=estudiante_profile
    ).select_related('vacante', 'vacante__empresa')
    
    return render(request, 'postulaciones/ver_postulaciones.html', {
        'postulaciones': postulaciones,
        'titulo': 'Mis Postulaciones'
    })

class EmpresaRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        try:
            return hasattr(self.request.user, 'empresaprofile') and self.request.user.empresaprofile is not None
        except EmpresaProfile.DoesNotExist:
            return False
        
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            try:
                if hasattr(self.request.user, 'estudianteprofile') and self.request.user.estudianteprofile is not None:
                    return redirect('dashboards:dashboard_estudiante')
            except EstudianteProfile.DoesNotExist:
                pass # No tiene perfil de estudiante, sigue con la redirección por defecto

        return super().handle_no_permission()
    
# --- Vistas para la gestión de postulaciones por parte de las EMPRESAS ---
class PostulacionesVacantesEmpresaListView(EmpresaRequiredMixin, ListView):
    model = Vacante
    template_name = 'postulaciones/postulaciones_vacantes_empresa_lista.html'
    context_object_name = 'vacantes'

    def get_queryset(self):
        perfil_empresa = self.request.user.empresaprofile
        from django.db.models import Count
        return Vacante.objects.filter(empresa=perfil_empresa).annotate(
            total_postulaciones=Count('postulaciones')
        ).order_by('-fecha_publicada')
    
class PostulacionesEmpresaListView(EmpresaRequiredMixin, ListView):
    model = Postulacion
    template_name = 'postulaciones/postulaciones_empresa_lista.html'
    context_object_name = 'postulaciones'

    def get_queryset(self):
        vacante_id = self.kwargs['pk']
        perfil_empresa = self.request.user.empresaprofile

        self.vacante = get_object_or_404(
            Vacante,
            pk=vacante_id,
            empresa=perfil_empresa
        )
        
        return Postulacion.objects.filter(vacante=self.vacante).order_by('fecha_postulacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacante'] = self.vacante
        return context
    
class PostulacionEmpresaDetailView(EmpresaRequiredMixin, UpdateView):
    model = Postulacion
    form_class = PostulacionStatusUpdateForm
    template_name = 'postulaciones/postulacion_empresa_detalles.html'
    context_object_name = 'postulacion'

    def get_object(self, queryset = ...):
        postulacion_id = self.kwargs['pk']
        return get_object_or_404(
            Postulacion,
            pk=postulacion_id,
            vacante__empresa=self.request.user.empresaprofile
        )
    
    def get_success_url(self):
        return reverse_lazy('postulaciones:postulaciones_empresa_lista', kwargs={'pk': self.object.vacante.pk})