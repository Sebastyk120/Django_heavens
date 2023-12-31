from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from .choices import negociacion, tipo_muestreo
from nomina import models as modelos_nomina


class Bodega(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Empaque(models.Model):
    tipo_empaque = models.CharField(max_length=100, verbose_name="Tipo De Empaque")
    tara = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="Tara")

    class Meta:
        ordering = ['tipo_empaque']

    def __str__(self):
        return self.tipo_empaque + "Tara:" + str(self.tara)


class Fruta(models.Model):
    nombre_fruta = models.CharField(max_length=100)

    class Meta:
        ordering = ['nombre_fruta']

    def __str__(self):
        return self.nombre_fruta


class Defectos(models.Model):
    nombre_defectos = models.CharField(max_length=100)

    class Meta:
        ordering = ['nombre_defectos']

    def __str__(self):
        return self.nombre_defectos


class Item(models.Model):
    numero_item = models.CharField(max_length=100, verbose_name="Numero De Item")
    kilos_netos = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    fruta = models.ForeignKey(Fruta, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, default='Recibo')
    tipo_negociacion = models.CharField(max_length=50, choices=negociacion, verbose_name="Tipo De Negociacion")
    porcen_muestreo = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True,
                                          blank=True)
    tipo_muestreo = models.CharField(max_length=50, choices=tipo_muestreo, verbose_name="Tipo De Muestreo", null=True,
                                     blank=True)
    lider_muestreo = models.CharField(max_length=50, verbose_name="Lider De Muestreo", null=True, blank=True)
    emp_muestreo = models.IntegerField(verbose_name="Cantidad Empaque Muestreo", null=True, blank=True)
    tip_empaque = models.ForeignKey(Empaque, on_delete=models.SET_NULL, null=True, blank=True)
    emp_nacional = models.IntegerField(verbose_name="Cantidad Empaque Nacional", null=True, blank=True)
    defectos = models.CharField(max_length=500, null=True, blank=True)
    patinador = models.ForeignKey(modelos_nomina.Empleados, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, verbose_name="Usuario")
    numero_remsion = models.IntegerField(verbose_name="Numero De Remision", null=True, blank=True)
    conductor = models.CharField(max_length=50, verbose_name="Conductor o Proveedor", null=True, blank=True)
    cedula_pro = models.IntegerField(verbose_name="Cedula Provedoor o Conductor", null=True, blank=True)

    def save(self, *args, **kwargs):
        update_fields = {}
        if self.tipo_negociacion:
            update_fields['porcen_muestreo'] = self.porcen_muestreo
        if self.tipo_muestreo:
            update_fields['tipo_muestreo'] = self.tipo_muestreo
        if self.lider_muestreo:
            update_fields['lider_muestreo'] = self.lider_muestreo
        if self.tipo_muestreo:
            update_fields['tipo_muestreo'] = self.tipo_muestreo
        if self.emp_muestreo:
            update_fields['emp_muestreo'] = self.emp_muestreo
        if self.tip_empaque:
            update_fields['tip_empaque_id'] = self.tip_empaque_id
        if self.emp_nacional:
            update_fields['emp_nacional'] = self.emp_nacional
        if self.defectos:
            update_fields['defectos'] = self.defectos
        if self.patinador:
            update_fields['patinador_id'] = self.patinador_id
        if self.numero_remsion:
            update_fields['numero_remsion'] = self.numero_remsion
        if self.conductor:
            update_fields['conductor'] = self.conductor
        if self.cedula_pro:
            update_fields['cedula_pro'] = self.cedula_pro
        if update_fields:
            Item.objects.filter(numero_item=self.numero_item).update(**update_fields)
        if isinstance(self.defectos, list):
            self.defectos = ','.join(self.defectos)
        super().save(*args, **kwargs)

    def clean(self):
        if self.defectos:
            self.defectos = self.defectos.split(',')
        super().clean()

    class Meta:
        ordering = ['numero_item']

    def __str__(self):
        return f"{self.numero_item} - {self.bodega} - {self.kilos_netos} - {self.fruta}"


class Movimiento(models.Model):
    item_historico = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kilos Netos")
    bodega_origen = models.ForeignKey(Bodega, related_name='movimientos_salida', on_delete=models.CASCADE)
    bodega_destino = models.ForeignKey(Bodega, related_name='movimientos_entrada', on_delete=models.CASCADE)
    fruta = models.CharField(max_length=50)
    t_negociacion = models.CharField(max_length=50, verbose_name="Tipo Negociacion")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Movimiento")
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return f"{self.item_historico} - {self.cantidad} - {self.bodega_origen} - {self.bodega_destino} - {self.fecha}"


class Movimientosmuestreo(models.Model):
    item_historico_muestreo = models.CharField(max_length=100)
    porcentaje_muestreo = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                              verbose_name="Porcentaje Muestreado")
    tipo_muestreo = models.CharField(max_length=50, verbose_name="Tipo Muestreo")
    lider_muestreo = models.CharField(max_length=50, verbose_name="Lider De Muestreo")
    empaque_muestreo = models.CharField(max_length=50, verbose_name="Cantidad Empaque Muestreo")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Muestreo")
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return f"{self.item_historico_muestreo} - {self.porcentaje_muestreo} - {self.tipo_muestreo}"
