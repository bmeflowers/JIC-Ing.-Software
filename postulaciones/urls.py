from django.urls import path
from . import views

app_name = 'postulaciones'

urlpatterns = [
    path('postular/<int:vacante_id>/', views.postular_vacante, name='postular_vacante'),
    path('mis-postulaciones/', views.ver_postulaciones, name='ver_postulaciones'),
    
    path('empresa/mis-vacantes-postulaciones/', views.PostulacionesVacantesEmpresaListView.as_view(), name='postulaciones_vacantes_empresa_lista'),
    path('empresa/vacante/<int:pk>/postulaciones/', views.PostulacionesEmpresaListView.as_view(), name='postulaciones_empresa_lista'),
    path('empresa/postulacion/<int:pk>/detalles/', views.PostulacionEmpresaDetailView.as_view(), name='postulacion_empresa_detalles')
]