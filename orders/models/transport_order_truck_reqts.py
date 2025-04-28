
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from .transport_order import TransportOrder
from ws import WSClassifiers


def validate_temperature(value):
    min_value = -273
    max_value = 35
    if value > 35:
        raise ValidationError(f'The temperature must not be set above {max_value} ℃')
    if value < min_value:
        raise ValidationError(f'The temperature must not be set below {min_value} ℃')
    return value

class TransportOrderTruckReqts(models.Model):
    
    class Meta:
        indexes = [
            models.Index(fields=['order']),
        ]
        ordering = ['order']
        verbose_name = 'Требования к транспорту заказа'
        verbose_name_plural = 'Требования к транспорту заказа'

    order = models.OneToOneField(
        TransportOrder,
        on_delete = models.CASCADE,
        blank = False,
        verbose_name = 'Заказ'
    )

    weight = models.DecimalField(
        default = 0.000,
        max_digits = 15,
        decimal_places = 3,
        blank = False,
        verbose_name = 'Масса'
    )

    weight_unit = models.CharField(
        default = '',
        blank = False,
        verbose_name = 'Единица измерения массы'
    )

    volume = models.DecimalField(
        default = 0.00,
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        verbose_name = 'Объем'
    )

    volume_unit = models.CharField(
        default = '',
        blank = True,
        verbose_name = 'Единица измерения объема'
    )

    refrigeration = models.BooleanField(
        default = False,
        blank = False,
        verbose_name = 'Охлаждение'
    )

    temperature = models.SmallIntegerField(
        default = 0,
        validators = [validate_temperature],
        blank = True,
        verbose_name = 'Температура'
    )

    comment = models.CharField(
        max_length = 1024,
        default = '',
        blank = True,
        verbose_name = 'Комментарий'
    )

    repr = models.CharField(
        max_length = 255,
        default = '',
        blank = True,
        verbose_name = 'Заказ'
    )

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

@receiver(pre_save, sender=TransportOrderTruckReqts)
def update_repr(sender: TransportOrderTruckReqts, **kwargs):
    repr_weight = f'{sender.weight} {sender.weight_unit}'
    repr_volume = ''

    weight_unit, success = WSClassifiers.get_unit_by_code_str(code_str=sender.weight_unit)
    if success:
        repr_weight = f'{sender.weight} {weight_unit}'
    
    if sender.volume_unit:
        volume_unit, success = WSClassifiers.get_unit_by_code_str(code_str=sender.volume_unit)
        if success:
            repr_volume = f'{sender.volume} {volume_unit}'
        else:
            repr_volume = f'{sender.volume} {sender.volume_unit}'
    
    new_rep = f'{repr_weight} {repr_volume}'.rstrip()

    if sender.repr != new_rep:
        sender.repr = new_rep

@receiver(pre_save, sender=TransportOrderTruckReqts)
def clear_temperature(sender: TransportOrderTruckReqts, **kwargs):
    if not sender.refrigeration:
        sender.temperature = 0