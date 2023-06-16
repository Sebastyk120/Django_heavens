from django import forms
from .models import Item, Bodega


class MovimientoForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.exclude(bodega__nombre="Salida Total"))
    cantidad = forms.IntegerField()
    bodega_destino = forms.ModelChoiceField(queryset=Bodega.objects.exclude(id=1), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('item'):
            item = self.initial['item']
            self.fields['cantidad'].initial = item.kilos_netos

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        cantidad = cleaned_data.get('cantidad')
        bodega_destino = cleaned_data.get('bodega_destino')

        if item and cantidad:
            if cantidad > item.kilos_netos:
                raise forms.ValidationError(
                    f"Debes mover menos de ({item.kilos_netos}) kilos netos para el item {item}.")

            if cantidad < 0:
                raise forms.ValidationError("La cantidad de kilos a mover debe ser un número mayor a 0.")

            if cantidad == item.kilos_netos and not bodega_destino:
                raise forms.ValidationError("Debes seleccionar una bodega de destino para dar salida al item.")
