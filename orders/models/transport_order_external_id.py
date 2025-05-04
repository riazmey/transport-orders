
from django.db import models

from .marketplace import Marketplace
from .transport_order import TransportOrder


class TransportOrderExternalID(models.Model):

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['market', 'order', 'external_id'],
                name='unique_external_id')]

        indexes = [
            models.Index(fields=['market', 'order'], name='external_market_order_idx'),
            models.Index(fields=['market', 'order', 'external_id'], name='external_market_order_id_idx')]

        ordering = ['market', 'order', 'external_code', 'external_id']
        verbose_name = 'Идентификатор заказа'
        verbose_name_plural = 'Идентификаторы заказов'

    market = models.ForeignKey(
        Marketplace,
        on_delete = models.PROTECT,
        related_name = 'market_relate_external_id',
        blank = False,
        verbose_name = 'Площадка')
    
    order = models.ForeignKey(
        TransportOrder,
        on_delete = models.CASCADE,
        related_name = 'order_relate_external_id',
        blank = False,
        verbose_name = 'Заказ')

    external_id = models.CharField(
        max_length = 40,
        blank = False,
        verbose_name = 'Идентификатор')

    external_code = models.CharField(
        max_length = 40,
        default = '',
        blank = True,
        verbose_name = 'Код (человекочитаемый)')

    @property
    def repr(self) -> str:
        if self.order:
            return f'ID {self.order.repr}: {self.external_id}'[:255]
        else:
            return 'Идентификатор заказа (новый)'

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr
