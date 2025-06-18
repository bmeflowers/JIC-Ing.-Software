from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard_empresa(request):
    return render(request, 'dashboards/dashboard_empresa.html')

@login_required
def dashboard_estudiante(request):
    return render(request, 'dashboards/dashboard_estudiante.html')