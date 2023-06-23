from django.contrib import admin
from .models import Bodega, Item, Movimiento, Fruta, Defectos, Empaque


class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ("fecha",)


class MovimientoAdmin(admin.ModelAdmin):
    readonly_fields = ("fecha",)


# Modelos Inventario Tiempo Real
admin.site.register(Bodega)
admin.site.register(Item, ItemAdmin)
admin.site.register(Movimiento, MovimientoAdmin)
admin.site.register(Fruta)
admin.site.register(Defectos)
admin.site.register(Empaque)
