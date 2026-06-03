from django.contrib import admin
from django.urls import path
from . import views
from ventas.views import producto_precios

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('api/productos/<int:producto_id>/precios/', producto_precios, name='producto_precios'),
]
