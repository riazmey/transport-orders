
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .transport_order import TransportOrder
from orders.validators import validate_transport_order_truck_reqts_temperature
from ws import WSClassifiers


class TransportOrderTruckReqts(models.Model):
    
    class Meta:
        indexes = [models.Index(fields=['order'])]
        ordering = ['order']
        verbose_name = 'Требования к транспорту заказа'
        verbose_name_plural = 'Требования к транспорту заказа'

    order = models.OneToOneField(
        TransportOrder,
        on_delete = models.CASCADE,
        blank = False,
        verbose_name = 'Заказ')

    weight = models.DecimalField(
        default = 0.000,
        max_digits = 15,
        decimal_places = 3,
        blank = False,
        verbose_name = 'Масса')

    weight_unit = models.CharField(
        max_length = 4,
        default = '',
        blank = False,
        verbose_name = 'Единица измерения массы')

    volume = models.DecimalField(
        default = 0.00,
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        verbose_name = 'Объем')

    volume_unit = models.CharField(
        max_length = 4,
        default = '',
        blank = True,
        verbose_name = 'Единица измерения объема')

    refrigeration = models.BooleanField(
        default = False,
        blank = False,
        verbose_name = 'Охлаждение')

    temperature = models.SmallIntegerField(
        default = 0,
        validators = [validate_transport_order_truck_reqts_temperature],
        blank = True,
        verbose_name = 'Температура')

    comment = models.CharField(
        max_length = 1024,
        default = '',
        blank = True,
        verbose_name = 'Комментарий')

    repr = models.CharField(
        max_length = 255,
        default = '',
        blank = True,
        verbose_name = 'Требования к транспорту заказа')

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

@receiver(pre_save, sender=TransportOrderTruckReqts)
def update_repr(sender, instance: TransportOrderTruckReqts, **kwargs):
    repr_weight = f'{instance.weight} {instance.weight_unit}'
    repr_volume = ''

    weight_unit, success = WSClassifiers.get_unit_by_code_str(code_str=instance.weight_unit)
    if success:
        repr_weight = f'{instance.weight} {weight_unit}'
    
    if instance.volume_unit:
        volume_unit, success = WSClassifiers.get_unit_by_code_str(code_str=instance.volume_unit)
        if success:
            repr_volume = f'{instance.volume} {volume_unit}'
        else:
            repr_volume = f'{instance.volume} {instance.volume_unit}'
    
    new_rep = f'{repr_weight} {repr_volume}'.rstrip()[:255]

    if instance.repr != new_rep:
        instance.repr = new_rep

@receiver(pre_save, sender=TransportOrderTruckReqts)
def clear_temperature(sender, instance: TransportOrderTruckReqts, **kwargs):
    if not instance.refrigeration:
        instance.temperature = 0