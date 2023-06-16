from django.db import models
from django.utils import timezone


class Bodega(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Item(models.Model):
    numero_item = models.CharField(max_length=100)
    kilos_netos = models.PositiveIntegerField(default=0)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)

    class Meta:
        ordering = ['numero_item']

    def __str__(self):
        return f"{self.numero_item} - {self.bodega} - {self.kilos_netos}"


class Movimiento(models.Model):
    item_historico = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    bodega_origen = models.ForeignKey(Bodega, related_name='movimientos_salida', on_delete=models.CASCADE)
    bodega_destino = models.ForeignKey(Bodega, related_name='movimientos_entrada', on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.item_historico} - {self.cantidad} - {self.bodega_origen} - {self.bodega_destino} - {self.fecha}"
