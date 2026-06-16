from decimal import Decimal
from django.db import models
from proveedores.models import Proveedor
from productos.models import Producto


class Compra(models.Model):
    TIPOS = [
        ('CONTADO', 'Contado'),
        ('CREDITO', 'Crédito'),
    ]

    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='compras')
    fecha = models.DateField()
    factura = models.CharField(max_length=100, blank=True, verbose_name='Factura/Nota')
    tipo = models.CharField(max_length=20, choices=TIPOS, default='CONTADO')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo_pendiente = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['-fecha']

    def __str__(self):
        return f'Compra #{self.id} - {self.proveedor.nombre} ({self.fecha})'


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='compras')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalles de Compra'

    @property
    def subtotal(self):
        return self.cantidad * (self.precio_unitario or 0)

    def __str__(self):
        return f'{self.producto.codigo} - {self.cantidad} x Q{self.precio_unitario:.2f}'


class PagoCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='pagos')
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateField()
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pago a Proveedor'
        verbose_name_plural = 'Pagos a Proveedores'
        ordering = ['-fecha']

    def __str__(self):
        return f'Pago Q{self.monto:.2f} - {self.fecha}'
