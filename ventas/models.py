from decimal import Decimal
from django.db import models
from clientes.models import Cliente
from vendedores.models import Vendedor
from productos.models import Producto


class Venta(models.Model):
    ESTADOS = [
        ('ENVIADO', 'Enviado'),
        ('PENDIENTE', 'Pendiente'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ventas')
    vendedor = models.ForeignKey(Vendedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas')
    fecha = models.DateField()
    nota_envio = models.CharField(max_length=100, blank=True, verbose_name='Nota de envío')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    descripcion = models.TextField(blank=True)
    gastos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    detalle = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-fecha']

    @property
    def venta_total(self):
        return sum(d.precio_total for d in self.detalles.all())

    @property
    def costo_total(self):
        return sum(d.costo_total for d in self.detalles.all())

    @property
    def ganancia_total(self):
        return self.venta_total - self.costo_total - self.gastos

    @property
    def ganancia_pp(self):
        if self.venta_total:
            return (self.ganancia_total / self.venta_total) * 100
        return 0

    def __str__(self):
        return f'Venta #{self.id} - {self.cliente.nombre} ({self.fecha})'


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Venta'

    @property
    def precio_total(self):
        return self.cantidad * (self.precio_unitario or Decimal('0'))

    @property
    def costo_total(self):
        return self.cantidad * (self.costo_unitario or Decimal('0'))

    def save(self, *args, **kwargs):
        if self.precio_unitario is None and self.producto_id:
            self.precio_unitario = self.producto.precio_venta
        if self.costo_unitario is None and self.producto_id:
            self.costo_unitario = self.producto.costo_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.producto.codigo} - {self.cantidad} und.'
