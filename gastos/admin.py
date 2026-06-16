from django.contrib import admin
from .models import Gasto


@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'descripcion_corta', 'monto', 'fecha', 'proveedor']
    list_filter = ['tipo', 'fecha']
    search_fields = ['descripcion', 'proveedor__nombre']
    date_hierarchy = 'fecha'
    fieldsets = [
        (None, {
            'fields': ['tipo', 'descripcion', 'monto', 'fecha']
        }),
        ('Relacionado a', {
            'fields': ['proveedor', 'venta'],
            'classes': ['collapse']
        }),
    ]

    def descripcion_corta(self, obj):
        return obj.descripcion[:80]
    descripcion_corta.short_description = 'Descripción'
