from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion_corta', 'precio_venta', 'precio_venta2', 'precio_venta3', 'costo_unitario', 'proveedor', 'activo']
    list_filter = ['proveedor__nombre', 'activo']
    search_fields = ['codigo', 'descripcion', 'proveedor__nombre']
    ordering = ['codigo']
    fieldsets = [
        (None, {
            'fields': ['codigo', 'descripcion', 'imagen', 'proveedor', 'ultima_compra']
        }),
        ('Precios', {
            'fields': [
                ('precio_venta', 'precio_venta2', 'precio_venta3'), 'costo_unitario'
            ]
        }),
        ('Estado', {
            'fields': ['activo']
        }),
    ]

    def descripcion_corta(self, obj):
        return obj.descripcion[:60]
    descripcion_corta.short_description = 'Descripción'
