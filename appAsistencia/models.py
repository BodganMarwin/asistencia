from django.db import models
from django.contrib.auth.models import User

# Create your models here.    

class PasanteModel(models.Model):
    supervisor = models.ManyToManyField(User, related_name='pasantes')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    ci = models.CharField(max_length=10, unique=True)
    correo = models.EmailField(unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True, blank=True)
    estado = models.BooleanField(default=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    


    def __str__(self):
        return self.nombre + ' ' + self.apellido
    class Meta:
        db_table = 'pasante'
        verbose_name = 'Pasante'
        verbose_name_plural = 'Pasantes'

class AsistenciaModel(models.Model):
    pasante = models.ForeignKey(PasanteModel, on_delete=models.RESTRICT)
    fecha_asistencia = models.DateField()
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.pasante.nombre + ' ' + self.pasante.apellido + ' - ' + str(self.fecha_asistencia)
    
    class Meta:
        db_table = 'asistencia'
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        unique_together = ('pasante', 'fecha_asistencia')
