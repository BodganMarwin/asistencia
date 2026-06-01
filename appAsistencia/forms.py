# forms.py
from django import forms
from .models import PasanteModel, AsistenciaModel

class PasanteForm(forms.ModelForm):
    class Meta:
        model = PasanteModel
        fields = [
            'supervisor', 'nombre', 'apellido', 'ci', 'correo', 
            'telefono', 'fecha_nacimiento', 'fecha_inicio', 'fecha_fin', 'estado'
        ]
        widgets = {
            'supervisor': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'ci': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cédula de Identidad'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de contacto'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = AsistenciaModel
        fields = ['pasante', 'fecha_asistencia', 'hora_entrada', 'hora_salida']
        widgets = {
            'pasante': forms.Select(attrs={'class': 'form-select'}),
            'fecha_asistencia': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_entrada': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_salida': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }