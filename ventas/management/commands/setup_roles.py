from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Crea grupos de Vendedor y asigna permisos básicos'

    def handle(self, *args, **options):
        vendedor_group, _ = Group.objects.get_or_create(name='Vendedor')
        admin_group, _ = Group.objects.get_or_create(name='Autorizador')

        models_perms = {
            'cliente': ['view', 'add', 'change'],
            'producto': ['view'],
            'venta': ['view', 'add', 'change'],
            'cotizacion': ['view', 'add', 'change'],
            'proveedor': ['view'],
        }

        for model_name, actions in models_perms.items():
            for app in ['clientes', 'productos', 'ventas', 'cotizaciones', 'proveedores']:
                try:
                    ct = ContentType.objects.get(
                        app_label=app,
                        model=model_name
                    )
                    for action in actions:
                        perm = Permission.objects.get(
                            content_type=ct,
                            codename=f'{action}_{model_name}'
                        )
                        vendedor_group.permissions.add(perm)
                    break
                except ContentType.DoesNotExist:
                    continue

        self.stdout.write(self.style.SUCCESS('Grupo "Vendedor" creado con permisos básicos'))
        self.stdout.write(self.style.SUCCESS('Grupo "Autorizador" creado (asignar permisos manualmente)'))
