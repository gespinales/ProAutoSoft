from django.contrib import admin
from .models import Envio, ItemEnvio

class ItemEnvioInline(admin.TabularInline):
    model = ItemEnvio
    extra = 1

@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    list_display = ['id', 'destinatario', 'fecha_envio', 'transportista', 'venta_id']
    list_filter = ['fecha_envio', 'transportista']
    search_fields = ['destinatario', 'direccion_entrega']
    inlines = [ItemEnvioInline]
