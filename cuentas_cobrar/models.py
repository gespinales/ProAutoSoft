from django.db import models
from ventas.models import Venta


class CuentaCobrar(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('AL_DIA', 'Al día'),
        ('VENCIDO', 'Vencido'),
        ('PAGADO', 'Pagado'),
    ]

    venta = models.OneToOneField(Venta, on_delete=models.PROTECT, related_name='cuenta_cobrar')
    saldo_pendiente = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cuenta por Cobrar'
        verbose_name_plural = 'Cuentas por Cobrar'
        ordering = ['-creado']

    def __str__(self):
        return f'CxC #{self.venta.id} - {self.venta.cliente.nombre} - Q{self.saldo_pendiente:.2f}'


class Abono(models.Model):
    TIPOS = [
        ('EFECTIVO', 'Efectivo'),
        ('CHEQUE', 'Cheque'),
        ('DEPOSITO', 'Depósito'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('OTRO', 'Otro'),
    ]

    cuenta_cobrar = models.ForeignKey(CuentaCobrar, on_delete=models.CASCADE, related_name='abonos')
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateField()
    tipo = models.CharField(max_length=20, choices=TIPOS, default='EFECTIVO')
    numero_referencia = models.CharField(max_length=100, blank=True, verbose_name='# Boleta/Cheque')
    observaciones = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Abono'
        verbose_name_plural = 'Abonos'
        ordering = ['-fecha']

    def __str__(self):
        return f'Abono Q{self.monto:.2f} - {self.fecha}'
