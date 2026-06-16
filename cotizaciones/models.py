from decimal import Decimal
from django.db import models
from clientes.models import Cliente
from vendedores.models import Vendedor
from productos.models import Producto


class Cotizacion(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('ACEPTADA', 'Aceptada'),
        ('VENCIDA', 'Vencida'),
        ('CANCELADA', 'Cancelada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='cotizaciones')
    vendedor = models.ForeignKey(Vendedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='cotizaciones')
    fecha = models.DateField()
    valida_hasta = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    observaciones = models.TextField(blank=True)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['-fecha']

    @property
    def total(self):
        return sum(d.subtotal for d in self.detalles.all())

    def __str__(self):
        return f'Cotización #{self.id} - {self.cliente.nombre} ({self.fecha})'


class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    precio_nivel = models.CharField(max_length=20, blank=True, help_text='Nivel de precio usado (1, 2, 3, personalizado)')

    class Meta:
        verbose_name = 'Detalle de Cotización'
        verbose_name_plural = 'Detalles de Cotización'

    @property
    def subtotal(self):
        return self.cantidad * (self.precio_unitario or 0)

    def __str__(self):
        return f'{self.producto.codigo} - {self.cantidad} x Q{self.precio_unitario:.2f}'
