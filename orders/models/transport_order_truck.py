
from django.db import models
from .transport_order import TransportOrder


class  TransportOrderTruck(models.Model):
    
    class Meta:
        indexes = [
            models.Index(fields=['order']),
        ]
        ordering = ['code_str']
        verbose_name = 'Транспорт заказа'
        verbose_name_plural = 'Грузы транспортно-логистических заказов'

    order = models.ForeignKey(
        TransportOrder,
        on_delete=models.PROTECT,
        blank=False,
        verbose_name='Транспортно-логистический заказ'
    )

    name = models.CharField(
        max_length=150,
        default='',
        blank=False,
        verbose_name='Наименование'
    )

    weight = models.FloatField(
        default=0.00,
        blank=False,
        verbose_name='Масса'
    )

    weight_unit = models.CharField(
        default='',
        blank=True,
        verbose_name='Единица измерения массы'
    )

    volume = models.FloatField(
        default=0.00,
        blank=False,
        verbose_name='Объем'
    )

    volume_unit = models.CharField(
        default='',
        blank=True,
        verbose_name='Единица измерения объема'
    )

    comment = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name='Комментарий'
    )

    repr = models.CharField(
        max_length=255,
        default='',
        blank=True,
        verbose_name='Транспортно-логистический заказ'
    )

    def save(self, *args, **kwargs):
        if self.repr != self.name:
            self.repr = self.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr
