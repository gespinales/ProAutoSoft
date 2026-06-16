from django.db import models
from proveedores.models import Proveedor


class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', blank=True)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Precio venta 1')
    precio_venta2 = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Precio venta 2')
    precio_venta3 = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Precio venta 3')
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.PROTECT, null=True, blank=True,
        related_name='productos'
    )
    ultima_compra = models.DateField(null=True, blank=True, verbose_name='Última compra')
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.descripcion[:80]}'
