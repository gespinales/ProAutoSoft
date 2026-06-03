from django.db import models


class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    proveedor = models.CharField(max_length=200, blank=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.descripcion[:80]}'
