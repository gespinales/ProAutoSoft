from django.db import models
from ventas.models import Venta


class Envio(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT, related_name='envios')
    destinatario = models.CharField(max_length=200)
    telefono_destinatario = models.CharField(max_length=50, blank=True)
    direccion_entrega = models.TextField()
    transportista = models.CharField(max_length=100, blank=True, help_text='Nombre del transportista o empresa')
    fecha_envio = models.DateField()
    firma_recibido = models.TextField(blank=True, help_text='Nombre de quien recibe')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Envío'
        verbose_name_plural = 'Envíos'
        ordering = ['-fecha_envio']

    def __str__(self):
        return f'Envío #{self.id} - {self.destinatario}'


class ItemEnvio(models.Model):
    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, related_name='items')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    descripcion = models.CharField(max_length=300)

    class Meta:
        verbose_name = 'Ítem de Envío'
        verbose_name_plural = 'Ítems de Envío'

    def __str__(self):
        return f'{self.cantidad}x {self.descripcion[:50]}'
