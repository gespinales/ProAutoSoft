from django.db import models


class Cliente(models.Model):
    RUTAS = [
        ('HUE_7', 'Huehuetenango 7'),
        ('HUE_17', 'Huehuetenango 17'),
        ('XELA_2', 'Quetzaltenango 2'),
        ('TOTO', 'Totonicapán'),
        ('SM', 'San Marcos'),
        ('OTRA', 'Otra'),
    ]

    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=50, blank=True)
    direccion = models.TextField(blank=True)
    ruta = models.CharField(max_length=20, choices=RUTAS, blank=True)
    contacto = models.CharField(max_length=200, blank=True, help_text='Nombre de contacto')
    nit = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
