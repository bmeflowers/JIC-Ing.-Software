from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import EstudianteRegisterForm, EmpresaRegisterForm, EstudianteProfileForm, EmpresaProfileForm
from .models import EstudianteProfile, EmpresaProfile
from django.contrib.auth.decorators import login_required

def home (request):
    return render(request, 'home.html')

from django.contrib.auth import login

def registroEstudiante(request):
    if request.method == 'POST':
        form = EstudianteRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user._tipo_usuario = 'estudiante'  
            user.save()
            EstudianteProfile.objects.filter(user=user).update(
                carrera=form.cleaned_data['carrera'],
                semestre=form.cleaned_data['semestre'],
                habilidades=form.cleaned_data['habilidades'],
                cv=form.cleaned_data.get('cv')
            )
            login(request, user)
            return redirect('dashboard_estudiante')
    else:
        form = EstudianteRegisterForm()
    return render(request, 'users/registroEst.html', {'form': form})


def registroEmpresa(request):
    if request.method == 'POST':
        form = EmpresaRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user._tipo_usuario = 'empresa'
            user.save()
            EmpresaProfile.objects.filter(user=user).update(
                nombre_empresa=form.cleaned_data['nombre_empresa'],
                rubro=form.cleaned_data['rubro'],
                descripcion=form.cleaned_data['descripcion'],
                sitio_web=form.cleaned_data['sitio_web']
            )
            login(request, user)
            return redirect('dashboard_empresa')
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
    perfil = EstudianteProfile.objects.get(user=request.user)
    return render(request, 'users/perfilEst.html', {'perfil': perfil})

@login_required
def perfilEmpresa(request):
    perfil = EmpresaProfile.objects.get(user=request.user)
    return render(request, 'users/perfilEmp.html', {'perfil': perfil})

@login_required
def editar_perfil_estudiante(request):
    perfil = EstudianteProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = EstudianteProfileForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfilEstudiante')
    else:
        form = EstudianteProfileForm(instance=perfil)

    return render(request, 'users/editProfileEst.html', {'form': form})

@login_required
def editar_perfil_empresa(request):
    perfil = EmpresaProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = EmpresaProfileForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfilEmpresa')  
    else:
        form = EmpresaProfileForm(instance=perfil)

    return render(request, 'users/editProfileEmp.html', {'form': form})
