from django.contrib import admin
from .models import Cliente, Mesa, Reserva

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email')
    search_fields = ('nombre', 'telefono')

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'estado', 'capacidad', 'ubicacion')
    list_filter = ('estado', 'ubicacion')
    ordering = ('numero',)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha', 'hora_inicio', 'hora_fin', 'mesa_asignada', 'estado')
    list_filter = ('estado', 'fecha')