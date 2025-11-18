from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

# Gestión de Clientes 
class Cliente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo")
    telefono = PhoneNumberField(unique=True, verbose_name="Teléfono") 
    email = models.EmailField(null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    preferencias = models.TextField(blank=True, help_text="Vegetariano, Celiaco, etc.")
    notas = models.TextField(blank=True, verbose_name="Observaciones")

    def __str__(self):
        return self.nombre or f"Cliente {self.pk}"


# Gestión de Mesas 
class Mesa(models.Model):
    ESTADOS = [
        ('LIBRE', 'Libre'),       
        ('OCUPADA', 'Ocupada'),
        ('RESERVADA', 'Reservada'),
        ('LIMPIEZA', 'En Limpieza'),
    ]
    
    numero = models.IntegerField(unique=True, verbose_name="Número de Mesa") 
    capacidad = models.PositiveIntegerField(verbose_name="Capacidad Personas")
    ubicacion = models.CharField(max_length=50, verbose_name="Ubicación")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='LIBRE')

    # se usa para integración con Módulo 3 (que usa booleano 'ocupada')
    @property
    def ocupada(self):
        return self.estado == 'OCUPADA'

    def __str__(self):
        return f"Mesa {self.numero} ({self.get_estado_display()})"


#  Gestión de Reservas 
class Reserva(models.Model):
    ESTADOS_RESERVA = [
        ('CONFIRMADA', 'Confirmada'),
        ('LLEGO', 'Cliente Llegó'), 
        ('CANCELADA', 'Cancelada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    mesa_asignada = models.ForeignKey(Mesa, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField(default=timezone.localdate, verbose_name="Fecha Reserva")
    hora_inicio = models.TimeField(null=True, blank=True, verbose_name="Hora Inicio")
    hora_fin = models.TimeField(null=True, blank=True, verbose_name="Hora Fin")
    cantidad_personas = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS_RESERVA, default='CONFIRMADA')

    def __str__(self):
        inicio = self.hora_inicio.strftime('%H:%M') if self.hora_inicio else '??:??'
        fin = self.hora_fin.strftime('%H:%M') if self.hora_fin else '??:??'
        return f"Reserva {self.pk} - {self.cliente} ({self.fecha} {inicio}→{fin})"