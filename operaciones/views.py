from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic.edit import CreateView
from django_tables2 import SingleTableView

from .forms import InventarioRealForm, ItemForm, MovimientoSearchForm
from .models import Bodega, Item, Movimiento
from .tables import MovimientoTable, ItemTable, InventariorealTable


def inventariotr(request):
    return render(request, 'home_inventariotr.html')


# Movimientos. (Inventario Real Aux Admin)
def inventario_real(request):
    usuario = request.user
    if request.method == 'POST':
        form = InventarioRealForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            cantidad = form.cleaned_data['cantidad']
            bodega_destino = form.cleaned_data['bodega_destino']
            if cantidad > 0:
                if cantidad <= item.kilos_netos and item.bodega != bodega_destino:
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
                    return JsonResponse({'success': True})
                elif item.bodega == bodega_destino:
                    error_msg = f"La bodega de origen -> {item.bodega}, es igual a la bodega destino -> {bodega_destino}"
                    return JsonResponse({'success': False, 'error': error_msg})
                else:
                    error_msg = f"No hay suficiente stock disponible para dar salida a {cantidad} kilos netos. Kilos Netos disponibles: {item.kilos_netos}"
                    return JsonResponse({'success': False, 'error': error_msg})
            else:
                error_msg = "La cantidad de kilos netos debe ser mayor que 0."
                return JsonResponse({'success': False, 'error': error_msg})
    else:
        form = InventarioRealForm()
    for bodega in Bodega.objects.all():
        items_bodega = Item.objects.filter(bodega=bodega).distinct('numero_item')
        for item in items_bodega:
            cantidad_total = Item.objects.filter(numero_item=item.numero_item, bodega=bodega).aggregate(
                total=Sum('kilos_netos'))['total']
            item.kilos_netos = cantidad_total
            item.save()
    bodegas_excluidas = ["Devolucion", "Nacional", "Exportacion", "Perdida"]
    items = Item.objects.exclude(bodega__nombre__in=bodegas_excluidas)
    table = InventariorealTable(items)
    return render(request, 'inventariotr_mover_item.html', {'form': form, 'table': table})


# Prueba para inventario Real. -----------------------------------------////----------------------------------//:

class InventarioRealListView(SingleTableView):
    model = Item
    table_class = InventariorealTable
    template_name = 'inventariotr_list_item.html'

    def get_queryset(self):
        bodegas_excluidas = ["Devolucion", "Nacional", "Exportacion", "Perdida"]
        return self.model.objects.exclude(bodega__nombre__in=bodegas_excluidas)


class InventarioCreateView(CreateView):
    model = Item
    form_class = InventarioRealForm
    template_name = 'inventariotr_mover_item.html'
    success_url = '/intentariotr_items_list/'

    def get(self, request, *args, **kwargs):
        item_id = request.GET.get('item_id', None)
        if item_id:
            item = Item.objects.get(pk=item_id)
            form = self.form_class(initial={'item': item})
            return render(request, self.template_name, {'form': form})
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        usuario = self.request.user
        item = form.cleaned_data['item']
        cantidad = form.cleaned_data['cantidad']
        bodega_destino = form.cleaned_data['bodega_destino']
        if cantidad > 0:
            if cantidad <= item.kilos_netos and item.bodega != bodega_destino:
                try:
                    # Buscar el mismo Item y combinar los kilos en la misma bodega.
                    existing_item = Item.objects.get(numero_item=item.numero_item, bodega=bodega_destino)
                    existing_item.kilos_netos += cantidad
                    existing_item.save()
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
                return JsonResponse({'success': True})
            elif item.bodega == bodega_destino:
                error_msg = f"La bodega de origen -> {item.bodega}, es igual a la bodega destino -> {bodega_destino}"
                return JsonResponse({'success': False, 'error': error_msg})
            else:
                error_msg = f"No hay suficiente stock disponible para dar salida a {cantidad} kilos netos. Kilos Netos disponibles: {item.kilos_netos}"
                return JsonResponse({'success': False, 'error': error_msg})
        else:
            error_msg = "La cantidad de kilos netos debe ser mayor que 0."
            return JsonResponse({'success': False, 'error': error_msg})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'html': render_to_string(self.template_name, {'form': form})})


# Prueba para inventario Real. -----------------------------------------////----------------------------------//


# Tabla De Historico De Movimientos. (Inventario Real)
class MovimientoListView(SingleTableView):
    model = Movimiento
    table_class = MovimientoTable
    template_name = 'historico.html'
    form_class = MovimientoSearchForm

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.form_class(self.request.GET)
        if form.is_valid():
            item_busqueda = form.cleaned_data.get('item_busqueda')
            if item_busqueda:
                queryset = queryset.filter(item_historico__icontains=item_busqueda)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_busqueda'] = self.form_class(self.request.GET)
        return context


# Mostrar Tabla Recibo - Bodega Recibo (Inventario Real)
class ItemListView(SingleTableView):
    model = Item
    table_class = ItemTable
    template_name = 'recibo_items_list.html'

    def get_queryset(self):
        bodega_especifica = Bodega.objects.get(
            nombre='Recibo')
        return super().get_queryset().filter(bodega=bodega_especifica)


# Crear Tabla De Recibo - Crear Item - Modal (Inventario Real)
class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'recibo_crear_item.html'
    success_url = '/recibo_items/'

    def get_initial(self):
        initial = super().get_initial()
        bodega_predeterminada = Bodega.objects.get(nombre='Recibo')
        initial['bodega'] = bodega_predeterminada
        return initial

    def form_valid(self, form):
        numero_item = form.cleaned_data['numero_item']
        fruta = form.cleaned_data['fruta']
        bodega = form.cleaned_data['bodega']
        kilos_netos = form.cleaned_data['kilos_netos']

        if Item.objects.filter(numero_item=numero_item).exclude(fruta=fruta).exists():
            error_msg = f'Ya existe este Item {numero_item}, con fruta diferente, revise la fruta que esta ingresando: {fruta}.'
            return JsonResponse({'success': False, 'error': error_msg})

        # Buscar el item igual en la misma bodega con el mismo numero_item y fruta
        try:
            existing_item = Item.objects.get(numero_item=numero_item, fruta=fruta, bodega=bodega)
            existing_item.kilos_netos += kilos_netos  # Sumar los kilos_netos
            existing_item.save()
            Movimiento.objects.create(
                item_historico=existing_item.numero_item,
                cantidad=existing_item.kilos_netos,
                bodega_origen=existing_item.bodega,
                bodega_destino=existing_item.bodega,
                fruta=existing_item.fruta.nombre_fruta,
                t_negociacion=existing_item.tipo_negociacion,
                fecha=timezone.now(),
                user=existing_item.user
            )
            return JsonResponse({'success': True})
        except Item.DoesNotExist:
            pass

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
