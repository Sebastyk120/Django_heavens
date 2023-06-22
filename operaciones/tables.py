# tables.py

import django_tables2 as tables
from .models import Movimiento


class MovimientoTable(tables.Table):
    class Meta:
        model = Movimiento
        template_name = "django_tables2/bootstrap.html"  # Use this template for bootstrap4 styling
        fields = (
            "item_historico", "cantidad", "bodega_origen", "bodega_destino", "fecha")  # fields to show in the table
