from django.urls import path
from . import views

app_name = 'dashboards'

urlpatterns = [
    path('empresa/', views.dashboard_empresa, name='dashboard_empresa'),
    path('estudiante/', views.dashboard_estudiante, name='dashboard_estudiante'),
]