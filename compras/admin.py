from django.contrib import admin
from .models import Compra, DetalleCompra, PagoCompra


class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 1
    autocomplete_fields = ['producto']
    fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']
    readonly_fields = ['subtotal']


class PagoCompraInline(admin.TabularInline):
    model = PagoCompra
    extra = 0
    fields = ['monto', 'fecha']
    readonly_fields = ['creado']


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'proveedor', 'fecha', 'tipo', 'total', 'saldo_pendiente']
    list_filter = ['tipo', 'fecha', 'proveedor']
    search_fields = ['proveedor__nombre', 'factura']
    inlines = [DetalleCompraInline, PagoCompraInline]
    date_hierarchy = 'fecha'
    fieldsets = [
        (None, {
            'fields': ['proveedor', 'fecha', 'factura', 'tipo']
        }),
        ('Totales', {
            'fields': ['total', 'saldo_pendiente'],
            'classes': ['collapse']
        }),
        ('Observaciones', {
            'fields': ['observaciones'],
            'classes': ['collapse']
        }),
    ]
