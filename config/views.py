from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, F
from django.utils import timezone
from clientes.models import Cliente
from productos.models import Producto
from ventas.models import Venta, DetalleVenta
from cuentas_cobrar.models import CuentaCobrar


@login_required
def dashboard(request):
    now = timezone.now()
    inicio_mes = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    total_clientes = Cliente.objects.filter(activo=True).count()
    total_productos = Producto.objects.filter(activo=True).count()

    ventas_mes_qs = Venta.objects.filter(fecha__gte=inicio_mes)
    ventas_mes = DetalleVenta.objects.filter(
        venta__in=ventas_mes_qs
    ).aggregate(
        total=Sum(F('cantidad') * F('precio_unitario'))
    )['total'] or 0

    saldo_pendiente = CuentaCobrar.objects.exclude(
        estado='PAGADO'
    ).aggregate(total=Sum('saldo_pendiente'))['total'] or 0

    ultimas_ventas = Venta.objects.select_related('cliente').prefetch_related('detalles').order_by('-fecha')[:10]
    cuentas_pendientes = CuentaCobrar.objects.select_related(
        'venta__cliente'
    ).exclude(estado='PAGADO').order_by('-saldo_pendiente')[:10]

    return render(request, 'dashboard.html', {
        'total_clientes': total_clientes,
        'total_productos': total_productos,
        'ventas_mes': ventas_mes,
        'saldo_pendiente': saldo_pendiente,
        'ultimas_ventas': ultimas_ventas,
        'cuentas_pendientes': cuentas_pendientes,
    })
