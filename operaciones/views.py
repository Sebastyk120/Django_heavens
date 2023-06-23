from django.db.models import Sum
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView
from django_tables2 import SingleTableView
from django.utils import timezone
from django.shortcuts import redirect, render
from .forms import MovimientoForm, ItemForm
from .tables import MovimientoTable, ItemTable, InventarioTable
from .models import Bodega, Item, Movimiento


def home_operaciones2(request):
    return render(request, 'home_operaciones.html')


def inventariotr(request):
    return render(request, 'inventariotr.html')


class InventariorealTable(SingleTableView):
    table_class = InventarioTable
    queryset = Item.objects.exclude(bodega__nombre="Salida Total").filter(kilos_netos__gt=0, bodega__isnull=False)
    template_name = 'mover_item.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object_list = None

    def get_table_data(self):
        data = super().get_table_data()
        for bodega in Bodega.objects.all():
            items_bodega = data.filter(bodega=bodega).distinct('numero_item')
            for item in items_bodega:
                cantidad_total = data.filter(numero_item=item.numero_item, bodega=bodega).aggregate(
                    total=Sum('kilos_netos'))['total']
                item.kilos_netos = cantidad_total
                item.save()
        return data

    def post(self, request, *args, **kwargs):
        form = MovimientoForm(request.POST)
        if form.is_valid():
            usuario = request.user
            item_id = request.POST.get('item_id')  # Obtener el ID del item desde el formulario
            item = Item.objects.get(id=item_id)
            cantidad = form.cleaned_data['cantidad']
            bodega_destino = form.cleaned_data['bodega_destino']
            if cantidad > 0:
                if cantidad <= item.kilos_netos:
                    if item.bodega != bodega_destino:
                        if bodega_destino:
                            try:
                                item_destino = Item.objects.get(numero_item=item.numero_item, bodega=bodega_destino)
                                item_destino.kilos_netos += cantidad
                                item_destino.save()
                            except Item.DoesNotExist:
                                Item.objects.create(numero_item=item.numero_item, kilos_netos=cantidad,
                                                    bodega=bodega_destino, fruta=item.fruta,
                                                    tipo_negociacion=item.tipo_negociacion, user=usuario)
                        item.kilos_netos -= cantidad
                        item.save()
                        movimiento = Movimiento(item_historico=item.numero_item, cantidad=cantidad,
                                                bodega_origen=item.bodega,
                                                bodega_destino=bodega_destino, fruta=item.fruta,
                                                t_negociacion=item.tipo_negociacion, user=usuario)
                        movimiento.save()
                        if item.kilos_netos == 0:
                            item.delete()
                        return redirect('mover_item')
                    else:
                        form.add_error('cantidad',
                                       f"No hay suficiente stock disponible para dar salida a {cantidad} kilos netos.")
                else:
                    form.add_error('cantidad', "La cantidad de kilos netos debe ser mayor que 0.")
        self.object_list = self.get_table_data()
        context = self.get_context_data()
        return self.render_to_response(context)


# Tabla De Historico De Movimientos. (Inventario Real)
class MovimientoListView(SingleTableView):
    model = Movimiento
    table_class = MovimientoTable
    template_name = 'historico.html'


# Mostrar Tabla Recibo - Bodega Recibo (Inventario Real)
class ItemListView(SingleTableView):
    model = Item
    table_class = ItemTable
    template_name = 'recibo_items.html'

    def get_queryset(self):
        bodega_especifica = Bodega.objects.get(
            nombre='Recibo')
        return super().get_queryset().filter(bodega=bodega_especifica)


# Crear Tabla De Recibo - Crear Item - Modal (Inventario Real)
class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'crear_item.html'
    success_url = '/recibo_items/'

    def get_initial(self):
        initial = super().get_initial()
        bodega_predeterminada = Bodega.objects.get(nombre='Recibo')
        initial['bodega'] = bodega_predeterminada
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        item = form.save()
        Movimiento.objects.create(
            item_historico=item.numero_item,
            cantidad=item.kilos_netos,
            bodega_origen=item.bodega,
            bodega_destino=item.bodega,
            fruta=item.fruta.nombre_fruta,
            t_negociacion=item.tipo_negociacion,
            fecha=timezone.now(),
            user=item.user
        )
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'html': render_to_string(self.template_name, {'form': form})})
