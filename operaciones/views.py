from django.db.models import Sum
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView
from django_tables2 import SingleTableView
from django.utils import timezone
from django.shortcuts import redirect, render
from .forms import MovimientoForm, ItemForm
from .tables import MovimientoTable, ItemTable
from .models import Bodega, Item, Movimiento


def home_operaciones2(request):
    return render(request, 'home_operaciones.html')


def inventariotr(request):
    return render(request, 'inventariotr.html')


def mover_item(request):
    usuario = request.user
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
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
                                                t_negociacion=item.tipo_negociacion)
                        movimiento.save()
                        if item.kilos_netos == 0:
                            item.delete()

                    return redirect('mover_item')
                else:
                    form.add_error('cantidad',
                                   f"No hay suficiente stock disponible para dar salida a {cantidad} kilos netos.")
            else:
                form.add_error('cantidad', "La cantidad de kilos netos debe ser mayor que 0.")
    else:
        form = MovimientoForm()
    for bodega in Bodega.objects.all():
        items_bodega = Item.objects.filter(bodega=bodega).distinct('numero_item')
        for item in items_bodega:
            cantidad_total = Item.objects.filter(numero_item=item.numero_item, bodega=bodega).aggregate(
                total=Sum('kilos_netos'))['total']
            item.kilos_netos = cantidad_total
            item.save()
    items = Item.objects.exclude(bodega__nombre="Salida Total").filter(kilos_netos__gt=0, bodega__isnull=False)
    return render(request, 'mover_item.html', {'form': form, 'items': items})


class MovimientoListView(SingleTableView):
    model = Movimiento
    table_class = MovimientoTable
    template_name = 'historico.html'


class ItemListView(SingleTableView):
    model = Item
    table_class = ItemTable
    template_name = 'recibo_items.html'

    def get_queryset(self):
        bodega_especifica = Bodega.objects.get(
            nombre='Recibo')
        return super().get_queryset().filter(bodega=bodega_especifica)


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
