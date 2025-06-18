from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Vacante
from .forms import VacanteRegisterForm
from users.models import EmpresaProfile, EstudianteProfile

# Create your views here.
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

# --- Vistas CRUD para la gestión de vacantes por parte de las empresas ---

class VacanteEmpresaListView(EmpresaRequiredMixin, ListView):
    model = Vacante
    template_name = 'vacantes/vacante_empresa_lista.html'
    context_object_name = 'vacantes'

    def get_queryset(self):
        perfil_empresa = self.request.user.empresaprofile
        return Vacante.objects.filter(empresa=perfil_empresa).order_by('-fecha_publicada')

class VacanteEmpresaDetailView(EmpresaRequiredMixin, DetailView):
    model = Vacante
    template_name = 'vacantes/vacante_empresa_detalles.html'
    context_object_name = 'vacante'

    def get_queryset(self):
        perfil_empresa = self.request.user.empresaprofile
        return Vacante.objects.filter(empresa=perfil_empresa)

class VacanteCreateView(EmpresaRequiredMixin, CreateView):
    model = Vacante
    form_class = VacanteRegisterForm
    template_name = 'vacantes/vacante_form.html'
    success_url = reverse_lazy('vacantes:vacante_empresa_lista')

    def form_valid(self, form):
        perfil_empresa = self.request.user.empresaprofile
        form.instance.empresa = perfil_empresa
        return super().form_valid(form)
    
class VacanteUpdateView(EmpresaRequiredMixin, UpdateView):
    model = Vacante
    form_class = VacanteRegisterForm
    template_name = 'vacantes/vacante_form.html'
    success_url = reverse_lazy('vacantes:vacante_empresa_lista')

    def get_queryset(self):
        perfil_empresa = self.request.user.empresaprofile
        return Vacante.objects.filter(empresa=perfil_empresa)
    
class VacanteDeleteView(EmpresaRequiredMixin, DeleteView):
    model = Vacante
    template_name = 'vacantes/vacante_confirmar_eliminar.html'
    success_url = reverse_lazy('vacantes:vacante_empresa_lista')

    def get_queryset(self):
        perfil_empresa = self.request.user.empresaprofile
        return Vacante.objects.filter(company=perfil_empresa)
    
# --- Vistas para que los estudiantes BUSQUEN vacantes (públicas) ---
# Estas vistas no requieren CompanyRequiredMixin, pero sí podrían requerir LoginRequiredMixin
# si solo estudiantes logueados pueden ver las vacantes públicas
class VacantePublicaListView(ListView):
    model = Vacante
    template_name = 'vacantes/vacante_publica_lista.html'
    context_object_name = 'vacantes'
    paginate_by = 10 # Paginación para muchas vacantes

    def get_queryset(self):
        return Vacante.objects.filter(activo=True).order_by('-fecha_publicada')
    
class VacantePublicaDetailListView(DetailView):
    model = Vacante
    template_name = 'vacantes/vacante_publica_detalles.html'
    context_object_name = 'vacante'

    def get_queryset(self):
        return Vacante.objects.filter(activo=True)