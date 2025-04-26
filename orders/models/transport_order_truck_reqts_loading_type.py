
from django.db import models
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
            models.Index(fields=['order']),
        ]
        ordering = ['code_str']
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
        verbose_name = 'Требование к загрузке грузового транспорта'
    )

    def save(self, *args, **kwargs):
        if self.repr != self.name:
            self.repr = self.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr
