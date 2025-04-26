
from django.db import models
from .transport_order import TransportOrder


class TransportOrderTruckReqts(models.Model):
    
    class Meta:
        indexes = [
            models.Index(fields=['order']),
        ]
        ordering = ['code_str']
        verbose_name = 'Требования к транспорту заказа'
        verbose_name_plural = 'Требования к транспорту заказа'

    order = models.OneToOneField(
        TransportOrder,
        on_delete = models.CASCADE,
        blank = False,
        verbose_name = 'Транспортно-логистический заказ'
    )

    weight = models.FloatField(
        default = 0.00,
        blank = False,
        verbose_name = 'Масса'
    )

    weight_unit = models.CharField(
        default = '',
        blank = True,
        verbose_name = 'Единица измерения массы'
    )

    volume = models.FloatField(
        default = 0.00,
        blank = False,
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
        min_value = -273,
        max_value = 35,
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
        verbose_name = 'Транспортно-логистический заказ'
    )

    def save(self, *args, **kwargs):
        if self.repr != self.name:
            self.repr = self.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr
