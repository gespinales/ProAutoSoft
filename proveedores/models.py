from django.db import models


class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=50, blank=True)
    direccion = models.TextField(blank=True)
    contacto = models.CharField(max_length=200, blank=True, help_text='Nombre de contacto')
    nit = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
