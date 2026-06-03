from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion_corta', 'precio_venta', 'costo_unitario', 'proveedor', 'activo']
    list_filter = ['proveedor', 'activo']
    search_fields = ['codigo', 'descripcion', 'proveedor']
    ordering = ['codigo']

    def descripcion_corta(self, obj):
        return obj.descripcion[:60]
    descripcion_corta.short_description = 'Descripción'
