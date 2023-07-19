from django import forms
from .models import Item, Bodega, Defectos


class InventarioRealForm(forms.Form):
    bodegas_excluidas = ["Nacional", "Devolucion", "Exportacion", "Perdida"]
    item = forms.ModelChoiceField(queryset=Item.objects.exclude(bodega__nombre__in=bodegas_excluidas))
    cantidad = forms.DecimalField()
    bodegas_excluidas2 = ["Nacional", "Devolucion", "Exportacion", "Perdida", "Recibo"]
    bodega_destino = forms.ModelChoiceField(queryset=Bodega.objects.exclude(nombre__in=bodegas_excluidas2),
                                            required=True)

    def __init__(self, *args, **kwargs):
        kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        if 'item' in self.initial:
            item = self.initial['item']
            self.fields['cantidad'].initial = item.kilos_netos
            self.fields['item'].queryset = self.fields['item'].queryset.filter(pk=item.pk)

    """def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        cantidad = cleaned_data.get('cantidad')
        bodega_destino = cleaned_data.get('bodega_destino')

        if item and cantidad:
            if cantidad > item.kilos_netos:
                self.add_error('cantidad',
                               f"Debes mover menos de ({item.kilos_netos}) kilos netos para el item {item}.")

            if cantidad < 0:
                self.add_error('cantidad', "La cantidad de kilos a mover debe ser un número mayor a 0.")

            if cantidad == item.kilos_netos and not bodega_destino:
                self.add_error('bodega_destino', "Debes seleccionar una bodega de destino para dar salida al item.")

        return cleaned_data"""


class ItemForm(forms.ModelForm):
    """defectos = forms.MultipleChoiceField(
        choices=[(defecto.nombre_defectos, defecto.nombre_defectos) for defecto in Defectos.objects.all()],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )"""

    class Meta:
        model = Item
        fields = ['numero_item', 'kilos_netos', 'fruta', 'bodega', 'tipo_negociacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bodega_predeterminada = Bodega.objects.get(nombre='Recibo')
        self.fields['bodega'].initial = bodega_predeterminada
        self.fields['bodega'].disabled = True
        self.fields['numero_item'].widget.attrs.update({'oninput': 'this.value = this.value.toUpperCase()'})

    def clean_numero_item(self):
        numero_item = self.cleaned_data.get('numero_item')
        if numero_item:
            numero_item = "R" + numero_item.upper()
        return numero_item

    """if self.instance and self.instance.defectos:
            self.fields['defectos'].initial = self.instance.defectos.split(',')

    def clean_defectos(self):
        defectos = self.cleaned_data.get('defectos')
        if defectos:
            return ','.join(defectos)
        return defectos"""


# Boton (Buscar Item, todos los modulos.)
class SearchForm(forms.Form):
    item_busqueda = forms.CharField(max_length=256, required=False)


# Formulario De Muestreo Porcentajes
class MuestreoForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['numero_item', 'porcen_muestreo', 'tipo_muestreo', 'lider_muestreo', 'emp_muestreo']

    def __init__(self, *args, **kwargs):
        super(MuestreoForm, self).__init__(*args, **kwargs)
        self.fields['numero_item'].widget.attrs['readonly'] = True


