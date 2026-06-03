from django.contrib import admin
from django import forms
from .models import Venta, DetalleVenta


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['precio_unitario'].widget = forms.TextInput(attrs={'readonly': True})
        self.fields['costo_unitario'].widget = forms.TextInput(attrs={'readonly': True})
        self.fields['cantidad'].widget = forms.TextInput(attrs={'inputmode': 'decimal'})


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    form = DetalleVentaForm
    extra = 1
    autocomplete_fields = ['producto']
    fields = ['producto', 'cantidad', 'precio_unitario', 'costo_unitario']

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return self.extra


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha', 'venta_total_display', 'estado']
    list_filter = ['estado', 'fecha']
    search_fields = ['cliente__nombre', 'nota_envio']
    inlines = [DetalleVentaInline]
    readonly_fields = ['venta_total_display', 'costo_total_display', 'ganancia_total_display', 'ganancia_pp_display']

    class Media:
        js = ['admin/js/detalle_venta.js']
        css = {'all': ['admin/css/detalle_venta.css']}
    date_hierarchy = 'fecha'
    fieldsets = [
        (None, {
            'fields': ['cliente', 'vendedor', 'fecha', 'estado', 'nota_envio']
        }),
        ('Totales', {
            'fields': [
                'venta_total_display', 'costo_total_display',
                'ganancia_total_display', 'ganancia_pp_display', 'gastos'
            ]
        }),
        ('Información adicional', {
            'fields': ['descripcion', 'detalle'],
            'classes': ['collapse']
        }),
    ]

    def venta_total_display(self, obj):
        return f'Q{obj.venta_total:,.2f}'
    venta_total_display.short_description = 'Venta Total'

    def costo_total_display(self, obj):
        return f'Q{obj.costo_total:,.2f}'
    costo_total_display.short_description = 'Costo Total'

    def ganancia_total_display(self, obj):
        return f'Q{obj.ganancia_total:,.2f}'
    ganancia_total_display.short_description = 'Ganancia Total'

    def ganancia_pp_display(self, obj):
        return f'{obj.ganancia_pp:.2f}%'
    ganancia_pp_display.short_description = 'Ganancia %'
