from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # Corregido: UserPassesTestMixin
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

class EmpresaRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):  # Corregido el nombre del mixin
    def test_func(self):
        return hasattr(self.request.user, 'empresaprofile')

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'estudianteprofile'):
                return redirect('dashboards:dashboard_estudiante')
        return super().handle_no_permission()

class VacanteEmpresaListView(EmpresaRequiredMixin, ListView):
    model = Vacante
    template_name = 'vacantes/vacante_empresa_lista.html'
    context_object_name = 'vacantes'

    def get_queryset(self):
        return Vacante.objects.filter(
            empresa=self.request.user.empresaprofile
        ).order_by('-fecha_publicada')

class VacanteEmpresaDetailView(EmpresaRequiredMixin, DetailView):
    model = Vacante
    template_name = 'vacantes/vacante_empresa_detalles.html'
    context_object_name = 'vacante'

    def get_queryset(self):
        return Vacante.objects.filter(empresa=self.request.user.empresaprofile)

class VacanteCreateView(EmpresaRequiredMixin, CreateView):
    model = Vacante
    form_class = VacanteRegisterForm
    template_name = 'vacantes/vacante_form.html'
    success_url = reverse_lazy('vacantes:vacante_empresa_lista')

    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresaprofile
        return super().form_valid(form)

class VacanteUpdateView(EmpresaRequiredMixin, UpdateView):
    model = Vacante
    form_class = VacanteRegisterForm
    template_name = 'vacantes/vacante_form.html'
    success_url = reverse_lazy('vacantes:vacante_empresa_lista')

    def get_queryset(self):
        return Vacante.objects.filter(empresa=self.request.user.empresaprofile)

class VacanteDeleteView(EmpresaRequiredMixin, DeleteView):
    model = Vacante
    template_name = 'vacantes/vacante_confirmar_eliminar.html'
    success_url = reverse_lazy('vacantes:vacante_empresa_lista')

    def get_queryset(self):
        return Vacante.objects.filter(empresa=self.request.user.empresaprofile)

class VacantePublicaListView(ListView):
    model = Vacante
    template_name = 'vacantes/vacante_publica_lista.html'
    context_object_name = 'vacantes'
    paginate_by = 10

    def get_queryset(self):
        return Vacante.objects.filter(activo=True).order_by('-fecha_publicada')

# Cambiado el nombre para coincidir con urls.py
class VacantePublicaDetailListView(DetailView):  # Antes era VacantePublicaDetailView
    model = Vacante
    template_name = 'vacantes/vacante_publica_detalles.html'
    context_object_name = 'vacante'

    def get_queryset(self):
        return Vacante.objects.filter(activo=True)