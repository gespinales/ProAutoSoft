from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Vendedor

class VendedorInline(admin.StackedInline):
    model = Vendedor
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [VendedorInline]
    list_display = ['username', 'first_name', 'last_name', 'is_staff', 'get_comision']

    def get_comision(self, obj):
        v = getattr(obj, 'vendedor', None)
        return f'{v.comision_porcentaje}%' if v else '-'
    get_comision.short_description = 'Comisión'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'comision_porcentaje', 'activo']
    list_filter = ['activo']
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name']

    def nombre(self, obj):
        return str(obj)
