
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .enum_truck_loading_type import EnumTruckLoadingType
from .transport_order_truck_reqts import TransportOrderTruckReqts


class TransportOrderTruckReqtsLoadingType(models.Model):
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order_truck_reqts', 'loading_type'],
                name='unique_order_truck_reqts_per_loading_type'
            )
        ]
        indexes = [
            models.Index(fields=['order_truck_reqts']),
        ]
        ordering = ['order_truck_reqts', 'loading_type']
        verbose_name = 'Требование к загрузке грузового транспорта'
        verbose_name_plural = 'Требования к загрузке грузовых транспортов'

    order_truck_reqts = models.ForeignKey(
        TransportOrderTruckReqts,
        on_delete = models.CASCADE,
        blank = False,
        verbose_name = 'Требование к транспорту заказа'
    )

    loading_type = models.ForeignKey(
        EnumTruckLoadingType,
        on_delete = models.PROTECT,
        blank = False,
        verbose_name = 'Тип загрузки'
    )

    repr = models.CharField(
        max_length = 255,
        default = '',
        blank = True,
        verbose_name = 'Требование к загрузке грузового транспорта'
    )

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

@receiver(pre_save, sender=TransportOrderTruckReqtsLoadingType)
def update_repr(sender: TransportOrderTruckReqtsLoadingType, **kwargs):
    order_truck_reqts = TransportOrderTruckReqts.objects.get(id=sender.order_truck_reqts)
    loading_type = EnumTruckLoadingType.objects.get(id=sender.loading_type)
    new_repr = f'{order_truck_reqts.repr}: {loading_type.repr} загрузка'
    if sender.repr != new_repr:
        sender.repr = new_repr