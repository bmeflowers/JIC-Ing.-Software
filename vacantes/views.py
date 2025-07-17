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

from django.db.models import Q

def vacante_publica_lista(request):
    session_key = 'vacante_ids_randomizadas'
    ubicacion_filtro = request.GET.get('ubicacion')
    texto_busqueda = request.GET.get('q', '').strip()
    location_select = request.GET.get('location', '').strip()

    LUGARES_PANAMA = [
        'panamá', 'ciudad de panamá', 'panama', 'colón', 'chiriquí', 'david',
        'veraguas', 'santiago', 'coclé', 'aguadulce', 'herrera', 'los santos',
        'bocas del toro', 'darien', 'chepo', 'panamá oeste', 'arraiján',
        'la chorrera', 'san miguelito'
    ]

    queryset = Vacante.objects.filter(activo=True)

    # Filtro por "nacional" o "internacional"
    if ubicacion_filtro == 'internacional':
        q_obj = Q()
        for lugar in LUGARES_PANAMA:
            q_obj |= Q(ubicacion__icontains=lugar)
        queryset = queryset.exclude(q_obj)

    elif ubicacion_filtro == 'nacional':
        q_obj = Q()
        for lugar in LUGARES_PANAMA:
            q_obj |= Q(ubicacion__icontains=lugar)
        queryset = queryset.filter(q_obj)

    if texto_busqueda:
        queryset = queryset.filter(
            Q(titulo__icontains=texto_busqueda) |
            Q(descripcion__icontains=texto_busqueda) |
            Q(empresa__nombre_empresa__icontains=texto_busqueda) |
            Q(ubicacion__icontains=texto_busqueda) |
            Q(duracion__icontains=texto_busqueda)
        )

    # Filtro por ubicación exacta (select)
    if location_select:
        queryset = queryset.filter(ubicacion__icontains=location_select.replace('-', ' '))

    # Obtener IDs
    ids = list(queryset.values_list('id', flat=True))

    # Determinar si hay filtros activos
    hay_filtros = texto_busqueda or location_select or ubicacion_filtro

    # Limpieza de sesión si los IDs ya no coinciden
    if session_key in request.session:
        session_ids = request.session[session_key]
        if set(session_ids) != set(ids):
            del request.session[session_key]

    # Aleatorizar según condiciones
    if not hay_filtros:
        # Siempre aleatorio si no hay filtros
        random.shuffle(ids)
    else:
        if session_key not in request.session or len(ids) != len(request.session[session_key]):
            random.shuffle(ids)
            request.session[session_key] = ids
        else:
            ids = request.session[session_key]

    # Paginación
    paginator = Paginator(ids, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Preservar orden aleatorio
    page_ids = page_obj.object_list
    preserved_order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(page_ids)])
    vacantes = Vacante.objects.filter(id__in=page_ids).order_by(preserved_order)

    return render(request, 'vacantes/vacante_publica_lista.html', {
        'vacantes': vacantes,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'total_vacantes': queryset.count(),
    })

class VacantePublicaDetailListView(DetailView):
    model = Vacante
    template_name = 'vacantes/vacante_publica_detalles.html'
    context_object_name = 'vacante'

    def get_queryset(self):
        return Vacante.objects.filter(activo=True)