from django.contrib import admin
from .models import Bodega, Item, Movimiento

# Modelos Inventario Tiempo Real
admin.site.register(Bodega)
admin.site.register(Item)
admin.site.register(Movimiento)
