from django.contrib.admin import AdminSite, site as default_admin_site


class ProAutoSoftAdminSite(AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        ordering = {
            'clientes': 10,
            'proveedores': 20,
            'vendedores': 30,
            'productos': 40,
            'compras': 50,
            'cotizaciones': 60,
            'ventas': 70,
            'cuentas_cobrar': 80,
            'envios': 90,
            'gastos': 100,
        }
        app_list.sort(key=lambda x: ordering.get(x['app_label'], 999))
        return app_list


admin_site = ProAutoSoftAdminSite(name='proautosoft_admin')

for model, admin_instance in default_admin_site._registry.items():
    admin_site.register(model, type(admin_instance))
