from django.contrib import admin
from .models import Bodega, Item, Movimiento, Fruta, Defectos, Empaque


class MovimientoAdmin(admin.ModelAdmin):
    readonly_fields = ("fecha",)


# Modelos Inventario Tiempo Real
admin.site.register(Bodega)
admin.site.register(Item)
admin.site.register(Movimiento, MovimientoAdmin)
admin.site.register(Fruta)
admin.site.register(Defectos)
admin.site.register(Empaque)
