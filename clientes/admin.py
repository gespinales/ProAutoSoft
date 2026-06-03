from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'ruta', 'activo']
    list_filter = ['ruta', 'activo']
    search_fields = ['nombre', 'telefono', 'contacto']
