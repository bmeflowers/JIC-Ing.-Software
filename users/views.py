from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import EstudianteRegisterForm, EmpresaRegisterForm
from .models import EstudianteProfile, EmpresaProfile
from django.contrib.auth.decorators import login_required

def home (request):
    return render(request, 'home.html')

def registroEstudiante(request):
    if request.method == 'POST':
        form = EstudianteRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            EstudianteProfile.objects.create(
                user=user,
                carrera=form.cleaned_data['carrera'],
                semestre=form.cleaned_data['semestre'],
                habilidades=form.cleaned_data['habilidades'],
                cv=form.cleaned_data.get('cv')
            )
            login(request, user)
            return redirect('perfilEstudiante')
    else:
        form = EstudianteRegisterForm()
    return render(request, 'users/registroEst.html', {'form': form})

def registroEmpresa(request):
    if request.method == 'POST':
        form = EmpresaRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            EmpresaProfile.objects.create(
                user=user,
                nombre_empresa=form.cleaned_data['nombre_empresa'],
                rubro=form.cleaned_data['rubro'],
                descripcion=form.cleaned_data['descripcion'],
                sitio_web=form.cleaned_data['sitio_web']
            )
            login(request, user)
            return redirect('perfilEmpresa')
    else:
        form = EmpresaRegisterForm()
    return render(request, 'users/registroEmp.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if hasattr(user, 'estudianteprofile'):
                return redirect('dashboard_estudiante')
            elif hasattr(user, 'empresaprofile'):
                return redirect('dashboard_empresa')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def perfilEstudiante(request):
    return render(request, 'users/perfilEst.html')

@login_required
def perfilEmpresa(request):
    return render(request, 'users/perfilEmp.html')

