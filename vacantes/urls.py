from django.urls import path
from .views import (
    VacanteEmpresaListView,
    VacanteEmpresaDetailView,
    VacanteCreateView,
    VacanteUpdateView,
    VacanteDeleteView,
    VacantePublicaListView,
    VacantePublicaDetailListView
)

app_name = 'vacantes'

urlpatterns = [
    path('empresa/mis-vacantes/', VacanteEmpresaListView.as_view(), name='vacante_empresa_lista'),
    path('empresa/crear/', VacanteCreateView.as_view(), name='crear_vacante'),
    path('empresa/<int:pk>/', VacanteEmpresaDetailView.as_view(), name='vacante_empresa_detalles'),
    path('empresa/<int:pk>/editar/', VacanteUpdateView.as_view(), name='actualizar_vacante'),
    path('empresa/<int:pk>/eliminar/', VacanteDeleteView.as_view(), name='eliminar_vacante'),
    path('', VacantePublicaListView.as_view(), name='vacante_publica_lista'),
    path('<int:pk>/', VacantePublicaDetailListView.as_view(), name='vacante_publica_detalles')
]
