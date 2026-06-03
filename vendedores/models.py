from django.db import models
from django.contrib.auth.models import User


class Vendedor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendedor')
    telefono = models.CharField(max_length=50, blank=True)
    comision_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'
        ordering = ['usuario__first_name']

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username
