from django.db import models


class Gasto(models.Model):
    TIPOS = [
        ('ENVIO', 'Envío'),
        ('GASOLINA', 'Gasolina'),
        ('SALARIO', 'Salario'),
        ('EMPAQUE', 'Empaque'),
        ('PAPELERIA', 'Papelería'),
        ('MANTENIMIENTO', 'Mantenimiento'),
        ('OTRO', 'Otro'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateField()
    proveedor = models.ForeignKey(
        'proveedores.Proveedor', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='gastos'
    )
    venta = models.ForeignKey(
        'ventas.Venta', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='gastos_operativos'
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Gasto Operativo'
        verbose_name_plural = 'Gastos Operativos'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.get_tipo_display()} - Q{self.monto:.2f} ({self.fecha})'
