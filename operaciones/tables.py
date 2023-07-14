import django_tables2 as tables
from .models import Movimiento, Item, Movimientosmuestreo


# Historicos (Inventario Real).
class MovimientoTable(tables.Table):
    class Meta:
        model = Movimiento
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            "item_historico", "cantidad", "bodega_origen", "bodega_destino", "fruta", "t_negociacion", "fecha", "user",)


# Recibo (Inventario Real)
class ItemTable(tables.Table):
    class Meta:
        model = Item
        template_name = "django_tables2/bootstrap5.html"
        fields = ("numero_item", "kilos_netos", "fruta", "bodega", "tipo_negociacion", "user")


# Base General de Items (Todos los Modulos)
class InventariorealTable(tables.Table):
    mover = tables.TemplateColumn(
        template_name='inventariotr_mover_button.html',
        orderable=False
    )

    class Meta:
        model = Item
        template_name = "django_tables2/bootstrap5.html"
        fields = ('numero_item', 'kilos_netos', 'bodega', 'fruta', 'tipo_negociacion', 'user',
                  'mover')
        attrs = {"class": "table"}


# Base para muestreo de calidad.
class MuestreoTable(tables.Table):
<<<<<<< HEAD
    muestreo = tables.TemplateColumn(
=======
    mover = tables.TemplateColumn(
>>>>>>> b7f5c408a72c6bf41db92399e252dd7048570347
        template_name='muestreo_muestra_button.html',
        orderable=False
    )

    class Meta:
        model = Item
        template_name = "django_tables2/bootstrap5.html"
        fields = ('numero_item', 'kilos_netos', 'bodega', 'fruta', 'tipo_negociacion', 'user',
                  'porcen_muestreo', 'tipo_muestreo', 'lider_muestreo', 'emp_muestreo')
        attrs = {"class": "table"}


# Base historico de muestreo.

class MovimientoMuestreoTable(tables.Table):
    class Meta:
        model = Movimientosmuestreo
        template_name = "django_tables2/bootstrap5.html"
