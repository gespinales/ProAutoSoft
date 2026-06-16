from django.contrib import admin
from .models import Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'contacto', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre', 'telefono', 'contacto', 'nit']
