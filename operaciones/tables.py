# tables.py

import django_tables2 as tables
from .models import Movimiento, Item


# Historicos (Inventario Real).
class MovimientoTable(tables.Table):
    class Meta:
        model = Movimiento
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            "item_historico", "cantidad", "bodega_origen", "bodega_destino", "fruta", "t_negociacion", "fecha", "user")


# Recibo (Inventario Real)
class ItemTable(tables.Table):
    # create = tables.TemplateColumn(template_name='mover_item_button.html', orderable=False, verbose_name='Crear Item')

    class Meta:
        model = Item
        template_name = "django_tables2/bootstrap5.html"
        fields = ("numero_item", "kilos_netos", "fruta", "bodega", "tipo_negociacion", "user")



