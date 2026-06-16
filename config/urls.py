from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .admin import admin_site
from ventas.views import producto_precios
from reportes import views as reportes_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin/', admin_site.urls),
    path('api/productos/<int:producto_id>/precios/', producto_precios, name='producto_precios'),
    path('reportes/historial-ventas/', reportes_views.historial_ventas, name='reporte_historial_ventas'),
    path('reportes/cuentas-cobrar/', reportes_views.cuentas_cobrar_reporte, name='reporte_cuentas_cobrar'),
    path('reportes/ganancias/', reportes_views.ganancias_venta, name='reporte_ganancias'),
    path('reportes/pedido-proveedor/', reportes_views.pedido_proveedor, name='reporte_pedido_proveedor'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
