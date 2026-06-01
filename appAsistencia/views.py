# views.py
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LogoutView
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
import datetime
from .models import PasanteModel, AsistenciaModel
from .forms import PasanteForm, AsistenciaForm

# ==========================================
# CRUD DE PASANTES
# ==========================================

class PasanteListView(ListView):
    model = PasanteModel
    template_name = 'pasantes/pasante_list.html'
    context_object_name = 'pasantes'
    paginate_by = 10
    queryset = PasanteModel.objects.all().order_by('-fecha_creacion')


class PasanteCreateView(SuccessMessageMixin, CreateView):
    model = PasanteModel
    form_class = PasanteForm
    template_name = 'pasantes/pasante_form.html'
    success_url = reverse_lazy('pasante_list')
    success_message = "El pasante %(nombre)s %(apellido)s fue registrado exitosamente."


class PasanteDetailView(DetailView):
    model = PasanteModel
    template_name = 'pasantes/pasante_detail.html'
    context_object_name = 'pasante'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir las asistencias del pasante al detalle
        context['asistencias'] = AsistenciaModel.objects.filter(pasante=self.object).order_by('-fecha_asistencia')
        return context


class PasanteUpdateView(SuccessMessageMixin, UpdateView):
    model = PasanteModel
    form_class = PasanteForm
    template_name = 'pasantes/pasante_form.html'
    success_url = reverse_lazy('pasante_list')
    success_message = "Los datos de %(nombre)s fueron actualizados correctamente."


class PasanteDeleteView(DeleteView):
    model = PasanteModel
    template_name = 'pasantes/pasante_confirm_delete.html'
    success_url = reverse_lazy('pasante_list')
    

# ==========================================
# CONTROL Y CRUD DE ASISTENCIAS
# ==========================================

class AsistenciaListView(ListView):
    model = AsistenciaModel
    template_name = 'asistencias/asistencia_list.html'
    context_object_name = 'asistencias'
    paginate_by = 15
    # Ordenamos por fecha y hora de entrada más reciente
    queryset = AsistenciaModel.objects.all().order_by('-fecha_asistencia', '-hora_entrada')

class AsistenciaMarcarView(CreateView):
    model = AsistenciaModel
    form_class = AsistenciaForm
    template_name = 'asistencias/asistencia_marcar.html'
    success_url = reverse_lazy('asistencia_marcar') # Redirige a la misma pantalla para el siguiente pasante

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Enviamos la fecha para mostrarla estática si JavaScript tarda en cargar
        context['fecha_hoy'] = datetime.date.today()
        return context

    def post(self, request, *args, **kwargs):
        ci_digitado = request.POST.get('ci_pasante')
        accion = request.POST.get('accion') # 'entrada' o 'salida'
        hoy = datetime.date.today()
        ahora = datetime.datetime.now().time()

        if not ci_digitado:
            messages.error(request, "Por favor, ingrese su número de Carnet de Identidad.")
            return redirect('asistencia_marcar')

        try:
            # Buscar al pasante por su C.I. y verificar que esté activo
            pasante = PasanteModel.objects.get(ci=ci_digitado, estado=True)
        except PasanteModel.DoesNotExist:
            messages.error(request, f"No se encontró ningún pasante activo con el C.I.: {ci_digitado}")
            return redirect('asistencia_marcar')

        if accion == 'entrada':
            # Validar si ya entró hoy
            existe_entrada = AsistenciaModel.objects.filter(pasante=pasante, fecha_asistencia=hoy).exists()
            if existe_entrada:
                messages.warning(request, f"{pasante.nombre}, ya registraste tu ENTRADA el día de hoy.")
            else:
                AsistenciaModel.objects.create(
                    pasante=pasante,
                    fecha_asistencia=hoy,
                    hora_entrada=ahora
                )
                messages.success(request, f"¡ENTRADA REGISTRADA! Bienvenido {pasante.nombre} {pasante.apellido}. Hora: {ahora.strftime('%H:%M')}")
                
        elif accion == 'salida':
            # Buscar la entrada previa de hoy para poder marcar la salida
            asistencia = AsistenciaModel.objects.filter(pasante=pasante, fecha_asistencia=hoy).first()
            if asistencia:
                if asistencia.hora_salida:
                    messages.warning(request, f"{pasante.nombre}, ya habías registrado tu SALIDA hoy.")
                else:
                    asistencia.hora_salida = ahora
                    asistencia.save()
                    messages.success(request, f"¡SALIDA REGISTRADA! Buen descanso {pasante.nombre}. Hora: {ahora.strftime('%H:%M')}")
            else:
                messages.error(request, f"{pasante.nombre}, no puedes marcar salida sin haber registrado una entrada previa hoy.")

        return redirect('asistencia_marcar')

# class AsistenciaMarcarView(CreateView):
#     """
#     Vista optimizada para que el pasante marque Entrada/Salida de forma rápida
#     sin tener que rellenar un formulario completo manualmente.
#     """
#     model = AsistenciaModel
#     form_class = AsistenciaForm
#     template_name = 'asistencias/asistencia_marcar.html'
#     success_url = reverse_lazy('asistencia_list')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Opcional: En un entorno real, filtrarías por el pasante ligado al usuario logueado.
#         # Aquí tomamos el primer pasante activo como simulación pedagógica.
#         pasante = PasanteModel.objects.filter(estado=True).first()
#         context['pasante_detectado'] = pasante
        
#         if pasante:
#             # Validar si ya existe un registro de asistencia para el pasante el día de hoy
#             context['asistencia_hoy'] = AsistenciaModel.objects.filter(
#                 pasante=pasante, 
#                 fecha_asistencia=datetime.date.today()
#             ).first()
#         return context

#     def post(self, request, *args, **kwargs):
#         pasante_id = request.POST.get('pasante_id')
#         accion = request.POST.get('accion') # 'entrada' o 'salida'
#         hoy = datetime.date.today()
#         ahora = datetime.datetime.now().time()

#         if not pasante_id:
#             messages.error(request, "No se ha detectado un pasante válido.")
#             return redirect('asistencia_marcar')

#         pasante = PasanteModel.objects.get(pk=pasante_id)

#         if accion == 'entrada':
#             # Verificar que no tenga entrada registrada hoy (Evitar duplicados por el unique_together)
#             existe = AsistenciaModel.objects.filter(pasante=pasante, fecha_asistencia=hoy).exists()
#             if existe:
#                 messages.warning(request, f"El pasante {pasante} ya registró su entrada el día de hoy.")
#             else:
#                 AsistenciaModel.objects.create(
#                     pasante=pasante,
#                     fecha_asistencia=hoy,
#                     hora_entrada=ahora
#                 )
#                 messages.success(request, f"¡Entrada registrada con éxito a las {ahora.strftime('%H:%M')}!")
                
#         elif accion == 'salida':
#             # Buscar el registro de hoy para registrar la salida
#             asistencia = AsistenciaModel.objects.filter(pasante=pasante, fecha_asistencia=hoy).first()
#             if asistencia:
#                 if asistencia.hora_salida:
#                     messages.warning(request, "Ya has registrado tu salida por el día de hoy.")
#                 else:
#                     asistencia.hora_salida = ahora
#                     asistencia.save()
#                     messages.success(request, f"¡Salida registrada con éxito a las {ahora.strftime('%H:%M')}! Que tenga un buen descanso.")
#             else:
#                 messages.error(request, "No puedes marcar salida sin haber registrado una entrada previamente.")

#         return redirect('asistencia_list')


class AsistenciaUpdateView(SuccessMessageMixin, UpdateView):
    """Permite al supervisor o administrador corregir horas manualmente."""
    model = AsistenciaModel
    form_class = AsistenciaForm
    template_name = 'asistencias/asistencia_form.html'
    success_url = reverse_lazy('asistencia_list')
    success_message = "El registro de asistencia fue corregido correctamente."


class AsistenciaDeleteView(DeleteView):
    model = AsistenciaModel
    template_name = 'asistencias/asistencia_confirm_delete.html'
    success_url = reverse_lazy('asistencia_list')
    success_message = "El registro de asistencia fue eliminado correctamente."