from django.contrib import admin
from .models import CuentaCobrar, Abono

class AbonoInline(admin.TabularInline):
    model = Abono
    extra = 0
    readonly_fields = ['creado']

@admin.register(CuentaCobrar)
class CuentaCobrarAdmin(admin.ModelAdmin):
    list_display = ['venta', 'cliente_nombre', 'saldo_pendiente', 'estado']
    list_filter = ['estado']
    search_fields = ['venta__cliente__nombre']
    inlines = [AbonoInline]
    readonly_fields = ['creado', 'actualizado']

    def cliente_nombre(self, obj):
        return obj.venta.cliente.nombre
    cliente_nombre.short_description = 'Cliente'

@admin.register(Abono)
class AbonoAdmin(admin.ModelAdmin):
    list_display = ['cuenta_cobrar', 'monto', 'fecha', 'tipo', 'numero_referencia']
    list_filter = ['tipo', 'fecha']
    search_fields = ['cuenta_cobrar__venta__cliente__nombre', 'numero_referencia']
