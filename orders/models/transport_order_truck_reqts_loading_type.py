
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

from .enum_truck_loading_type import EnumTruckLoadingType
from .transport_order_truck_reqts import TransportOrderTruckReqts


class TransportOrderTruckReqtsLoadingType(models.Model):
    
    class Meta:
        
        constraints = [
            models.UniqueConstraint(
                fields=['order_truck_reqts', 'loading_type'],
                name='unique_truck_reqts_load_type')]
        
        indexes = [models.Index(fields=['order_truck_reqts', 'loading_type'], name='truck_reqts_load_type_idx')]
        ordering = ['order_truck_reqts', 'loading_type']
        verbose_name = 'Требование к загрузке грузового транспорта'
        verbose_name_plural = 'Требования к загрузке грузовых транспортов'

    order_truck_reqts = models.ForeignKey(
        TransportOrderTruckReqts,
        on_delete = models.CASCADE,
        related_name = 'order_truck_reqts_relate_order_truck_reqts_loading_type',
        blank = False,
        verbose_name = 'Требование к транспорту заказа')

    loading_type = models.ForeignKey(
        EnumTruckLoadingType,
        on_delete = models.PROTECT,
        blank = False,
        verbose_name = 'Тип загрузки')

    @property
    def repr(self) -> str:
        if self.order_truck_reqts and self.loading_type:
            return f'{self.order_truck_reqts.repr}: {self.loading_type.repr} загрузка'[:255]
        else:
            'Требование к загрузке грузового транспорта'

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

@receiver(post_save, sender=TransportOrderTruckReqtsLoadingType)
def clear_cache(sender, instance: TransportOrderTruckReqtsLoadingType, **kwargs):
    cache.clear()