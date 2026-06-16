from django.contrib import admin, messages
from .models import Cotizacion, DetalleCotizacion
from ventas.models import Venta, DetalleVenta


class DetalleCotizacionInline(admin.TabularInline):
    model = DetalleCotizacion
    extra = 1
    autocomplete_fields = ['producto']
    fields = ['producto', 'cantidad', 'precio_unitario', 'precio_nivel', 'subtotal']
    readonly_fields = ['subtotal']


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha', 'valida_hasta', 'total_display', 'estado', 'venta_link']
    list_filter = ['estado', 'fecha']
    search_fields = ['cliente__nombre', 'vendedor__usuario__username']
    inlines = [DetalleCotizacionInline]
    date_hierarchy = 'fecha'
    actions = ['convertir_a_venta']
    fieldsets = [
        (None, {
            'fields': ['cliente', 'vendedor', 'fecha', 'valida_hasta', 'estado']
        }),
        ('Observaciones', {
            'fields': ['observaciones'],
            'classes': ['collapse']
        }),
    ]

    def total_display(self, obj):
        return f'Q{obj.total:,.2f}'
    total_display.short_description = 'Total'

    def venta_link(self, obj):
        venta = getattr(obj, 'venta_generada', None)
        if venta:
            from django.utils.html import format_html
            return format_html('<a href="/admin/ventas/venta/{}/change/">{}</a>', venta.id, f'Venta #{venta.id}')
        return '-'
    venta_link.short_description = 'Venta'

    def convertir_a_venta(self, request, queryset):
        for cotizacion in queryset:
            if hasattr(cotizacion, 'venta_generada') and cotizacion.venta_generada:
                self.message_user(request, f'Cotización #{cotizacion.id} ya tiene una venta asociada', level='WARNING')
                continue
            if cotizacion.estado != 'PENDIENTE':
                self.message_user(request, f'Cotización #{cotizacion.id} no está pendiente', level='WARNING')
                continue

            venta = Venta.objects.create(
                cliente=cotizacion.cliente,
                vendedor=cotizacion.vendedor,
                fecha=cotizacion.fecha,
                estado='PENDIENTE',
                descripcion=f'Convertida de Cotización #{cotizacion.id}',
                cotizacion=cotizacion,
            )

            for det in cotizacion.detalles.all():
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=det.producto,
                    cantidad=det.cantidad,
                    precio_unitario=det.precio_unitario,
                    costo_unitario=det.producto.costo_unitario,
                )

            cotizacion.estado = 'ACEPTADA'
            cotizacion.save()

            self.message_user(
                request,
                f'Cotización #{cotizacion.id} → Venta #{venta.id} creada exitosamente',
                level='SUCCESS'
            )

    convertir_a_venta.short_description = 'Convertir cotización seleccionada a Venta'
