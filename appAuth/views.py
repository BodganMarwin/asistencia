from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from appAuth.conexion import Autenticacion

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('pasante_list')
        else:
            messages.info(request, 'El nombre de Usuario o la contraseña son incorrectas')
    return render(request,'registration/login.html')

def log_out(request):
    logout(request)
    return redirect('login')

def index(request):
    return render(request, 'base.html')