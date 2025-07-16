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
from django.core.paginator import Paginator
from django.db.models import Case, When
import random


class EmpresaRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
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

def vacante_publica_lista(request):
    session_key = 'vacante_ids_randomizadas'

    if session_key not in request.session:
        ids = list(Vacante.objects.filter(activo=True).values_list('id', flat=True))
        random.shuffle(ids)
        request.session[session_key] = ids

    ids = request.session[session_key]

    paginator = Paginator(ids, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    page_ids = page_obj.object_list
    preserved_order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(page_ids)])
    vacantes = Vacante.objects.filter(id__in=page_ids).order_by(preserved_order)

    total_vacantes_activas = Vacante.objects.filter(activo=True).count()

    return render(request, 'vacantes/vacante_publica_lista.html', {
        'vacantes': vacantes,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'total_vacantes': total_vacantes_activas,
    })

class VacantePublicaDetailListView(DetailView):
    model = Vacante
    template_name = 'vacantes/vacante_publica_detalles.html'
    context_object_name = 'vacante'

    def get_queryset(self):
        return Vacante.objects.filter(activo=True)