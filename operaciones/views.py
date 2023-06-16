from django.db.models import Sum
from django.shortcuts import redirect, render
from .forms import MovimientoForm
from .models import Bodega, Item, Movimiento


def home_operaciones(request):
    return render(request, 'home_operaciones.html')


def mover_item(request):
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
                                                    bodega=bodega_destino)
                        item.kilos_netos -= cantidad
                        item.save()
                        movimiento = Movimiento(item_historico=item.numero_item, cantidad=cantidad, bodega_origen=item.bodega,
                                                bodega_destino=bodega_destino)
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
