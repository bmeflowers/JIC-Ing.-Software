from django.urls import path
from . import views

app_name = 'postulaciones'

urlpatterns = [
    path('postular/<int:vacante_id>/', views.postular_vacante, name='postular_vacante'),
    path('mis-postulaciones/', views.ver_postulaciones, name='ver_postulaciones'),
]