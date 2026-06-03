from django.http import JsonResponse
from productos.models import Producto


def producto_precios(request, producto_id):
    try:
        p = Producto.objects.get(id=producto_id)
        return JsonResponse({
            'precio_venta': str(p.precio_venta),
            'costo_unitario': str(p.costo_unitario),
            'codigo': p.codigo,
            'descripcion': p.descripcion,
        })
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
