from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/estudiante/', views.registroEstudiante, name='registroEstudiante'),
    path('registro/empresa/', views.registroEmpresa, name='registroEmpresa'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/estudiante/', views.perfilEstudiante, name='perfilEstudiante'),
    path('perfil/estudiante/editar/', views.editar_perfil_estudiante, name='editarPerfilEstudiante'),
    path('perfil/empresa/', views.perfilEmpresa, name='perfilEmpresa'),
    path('perfil/empresa/editar/', views.editar_perfil_empresa, name='editarPerfilEmpresa'),
]