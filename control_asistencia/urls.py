"""
URL configuration for control_asistencia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from appAsistencia.views import *
from appAuth.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    
    path('', login_required(PasanteListView.as_view()), name='pasante_list'),
    path('pasantes/nuevo/', login_required(PasanteCreateView.as_view()), name='pasante_create'),
    path('pasantes/<int:pk>/', login_required(PasanteDetailView.as_view()), name='pasante_detail'),
    path('pasantes/<int:pk>/editar/', login_required(PasanteUpdateView.as_view()), name='pasante_update'),
    path('pasantes/<int:pk>/eliminar/', login_required(PasanteDeleteView.as_view()), name='pasante_delete'),
    
    path('asistencias/', AsistenciaListView.as_view(), name='asistencia_list'),
    path('asistencias/marcar/', AsistenciaMarcarView.as_view(), name='asistencia_marcar'),
    path('asistencias/<int:pk>/editar/', AsistenciaUpdateView.as_view(), name='asistencia_update'),
    path('asistencias/<int:pk>/eliminar/', AsistenciaDeleteView.as_view(), name='asistencia_delete'),
    
]
