
from django.db import models
from .marketplace import Marketplace
from .enum_transport_order_status import EnumTransportOrderStatus


class  TransportOrder(models.Model):
    
    class Meta:
        indexes = [
            models.Index(fields=['status']),
        ]
        ordering = ['code_str']
        verbose_name = 'Транспортно-логистический заказ'
        verbose_name_plural = 'Транспортно-логистические заказы'

    market = models.ForeignKey(
        Marketplace,
        on_delete=models.PROTECT,
        blank=False,
        verbose_name='Торговая площадка'
    )

    status = models.ForeignKey(
        EnumTransportOrderStatus,
        on_delete=models.PROTECT,
        blank=False,
        verbose_name='Статус'
    )

    currency = models.CharField(
        max_length=3,
        default='',
        blank=False,
        verbose_name='Валюта'
    )

    price = models.FloatField(
        default=0.00,
        blank=False,
        verbose_name='Цена'
    )

    rate_vat = models.CharField(
        max_length=3,
        default='',
        blank=False,
        verbose_name='Ставка НДС'
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

