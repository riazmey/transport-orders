
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .transport_order import TransportOrder
from orders.validators import validate_transport_order_truck_reqts_temperature
from ws.classifiers import WSClassifiers


class TransportOrderTruckReqts(models.Model):
    
    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['order'],
                name='unique_order_truck_reqts')]

        indexes = [models.Index(fields=['order'], name='order_truck_reqts_idx')]
        ordering = ['order']
        verbose_name = 'Требования к транспорту заказа'
        verbose_name_plural = 'Требования к транспорту заказа'

    order = models.OneToOneField(
        TransportOrder,
        on_delete = models.CASCADE,
        related_name = 'order_relate_truck_requirements',
        blank = False,
        verbose_name = 'Заказ')

    weight = models.FloatField(
        default = 0.000,
        blank = False,
        verbose_name = 'Масса')

    weight_unit = models.CharField(
        max_length = 4,
        default = '',
        blank = False,
        verbose_name = 'Единица измерения массы')

    volume = models.FloatField(
        default = 0.00,
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

    @property
    def repr(self) -> str:
        repr_weight = f'{self.weight} {self.weight_unit}'
        repr_volume = ''

        ws = WSClassifiers()
        weight_unit, success = ws.get_unit({'code_dec': self.weight_unit})
        if success:
            name = weight_unit.get('name')
            notation_national = weight_unit.get('notation_national')
            notation_international = weight_unit.get('notation_international')
            if notation_national:
                repr_weight = f'{self.weight} {notation_national}'
            elif notation_international:
                repr_weight = f'{self.weight} {notation_international}'
            elif name:
                repr_weight = f'{self.weight} {name}'
            else:
                repr_weight = f'{self.weight} {self.weight_unit}'

        if self.volume_unit:
            volume_unit, success = ws.get_unit({'code_dec': self.volume_unit})
            if success:
                name = volume_unit.get('name')
                notation_national = volume_unit.get('notation_national')
                notation_international = volume_unit.get('notation_international')
                if notation_national:
                    repr_volume = f'{self.volume} {notation_national}'
                elif notation_international:
                    repr_volume = f'{self.volume} {notation_international}'
                elif name:
                    repr_volume = f'{self.volume} {name}'
                else:
                    repr_volume = f'{self.volume} {self.volume_unit}'
            else:
                repr_volume = f'{self.volume} {self.volume_unit}'

        return f'Требования к транспорту {self.order}: {repr_weight}, {repr_volume}'.rstrip()[:255]

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

@receiver(pre_save, sender=TransportOrderTruckReqts)
def clear_temperature(sender, instance: TransportOrderTruckReqts, **kwargs):
    if not instance.refrigeration:
        instance.temperature = 0

@receiver(post_save, sender=TransportOrder)
def clear_cache(sender, instance: TransportOrder, **kwargs):
    cache.clear()