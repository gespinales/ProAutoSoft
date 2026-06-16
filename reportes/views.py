from datetime import date, timedelta
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, F, Q
from django.db.models.functions import TruncMonth, TruncWeek
from ventas.models import Venta
from cuentas_cobrar.models import CuentaCobrar, Abono


@staff_member_required
def historial_ventas(request):
    periodo = request.GET.get('periodo', 'mensual')
    trunc_fn = TruncMonth if periodo == 'mensual' else TruncWeek
    label = 'Mes' if periodo == 'mensual' else 'Semana'

    ventas = (
        Venta.objects
        .annotate(periodo=trunc_fn('fecha'))
        .values('periodo')
        .annotate(
            total_ventas=Sum(F('detalles__cantidad') * F('detalles__precio_unitario')),
            total_costos=Sum(F('detalles__cantidad') * F('detalles__costo_unitario')),
            total_gastos=Sum('gastos'),
        )
        .order_by('-periodo')
    )

    for v in ventas:
        v['ganancia'] = (v['total_ventas'] or 0) - (v['total_costos'] or 0) - (v['total_gastos'] or 0)
        if v['total_ventas']:
            v['margen'] = (v['ganancia'] / v['total_ventas']) * 100
        else:
            v['margen'] = 0

    return render(request, 'reportes/historial_ventas.html', {
        'ventas': ventas,
        'periodo': periodo,
        'label': label,
        'title': f'Historial de Ventas ({periodo.capitalize()})',
    })


@staff_member_required
def cuentas_cobrar_reporte(request):
    cuentas = CuentaCobrar.objects.filter(
        Q(estado='PENDIENTE') | Q(estado='VENCIDO')
    ).select_related('venta__cliente')

    ruta = request.GET.get('ruta', '')
    if ruta:
        cuentas = cuentas.filter(venta__cliente__ruta=ruta)

    rutas = CuentaCobrar.objects.filter(
        Q(estado='PENDIENTE') | Q(estado='VENCIDO')
    ).values_list('venta__cliente__ruta', flat=True).distinct().order_by()

    total_pendiente = cuentas.aggregate(total=Sum('saldo_pendiente'))['total'] or 0

    return render(request, 'reportes/cuentas_cobrar.html', {
        'cuentas': cuentas,
        'rutas': rutas,
        'ruta_seleccionada': ruta,
        'total_pendiente': total_pendiente,
        'title': 'Cuentas por Cobrar',
    })


@staff_member_required
def ganancias_venta(request):
    ventas = Venta.objects.all().select_related('cliente').prefetch_related('detalles')

    q = request.GET.get('q', '')
    fecha_desde = request.GET.get('desde', '')
    fecha_hasta = request.GET.get('hasta', '')

    if q:
        ventas = ventas.filter(cliente__nombre__icontains=q)
    if fecha_desde:
        ventas = ventas.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        ventas = ventas.filter(fecha__lte=fecha_hasta)

    return render(request, 'reportes/ganancias_venta.html', {
        'ventas': ventas,
        'q': q,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'title': 'Ganancias por Venta',
    })


@staff_member_required
def pedido_proveedor(request):
    from django.db.models import Count
    from ventas.models import DetalleVenta

    fecha_desde = request.GET.get('desde', '')
    fecha_hasta = request.GET.get('hasta', '')

    detalles = DetalleVenta.objects.filter(venta__estado__in=['PENDIENTE', 'ENVIADO', 'ENTREGADO'])

    if fecha_desde:
        detalles = detalles.filter(venta__fecha__gte=fecha_desde)
    if fecha_hasta:
        detalles = detalles.filter(venta__fecha__lte=fecha_hasta)

    pedidos = (
        detalles
        .values('producto__proveedor__nombre', 'producto__proveedor_id')
        .annotate(
            cantidad_total=Sum('cantidad'),
            total_productos=Count('producto', distinct=True),
        )
        .order_by('producto__proveedor__nombre')
    )

    return render(request, 'reportes/pedido_proveedor.html', {
        'pedidos': pedidos,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'title': 'Pedido Consolidado a Proveedores',
    })
