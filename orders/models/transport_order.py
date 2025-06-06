
from django.core.cache import cache

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.timezone import now

from .counterparty import Counterparty
from .enum_transport_order_status import EnumTransportOrderStatus
from .marketplace import Marketplace


class TransportOrder(models.Model):
    
    class Meta:
        indexes = [models.Index(fields=['market'], name='transport_order_market_idx')]
        ordering = ['modified', 'counterparty', 'status']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    market = models.ForeignKey(
        Marketplace,
        on_delete = models.PROTECT,
        blank = False,
        verbose_name = 'Площадка')

    counterparty = models.ForeignKey(
        Counterparty,
        on_delete = models.PROTECT,
        blank = True,
        verbose_name = 'Контрагент (заказчик)')

    modified = models.DateTimeField(
        blank = False,
        verbose_name = 'Дата изменения')

    status = models.ForeignKey(
        EnumTransportOrderStatus,
        on_delete = models.PROTECT,
        blank = False,
        verbose_name = 'Статус')

    currency = models.CharField(
        max_length = 3,
        default = '',
        blank = False,
        verbose_name = 'Валюта')
 
    price = models.FloatField(
        default = 0.00,
        blank = True,
        verbose_name = 'Цена')

    rate_vat = models.CharField(
        max_length = 20,
        default = '',
        blank = False,
        verbose_name = 'Ставка НДС')

    comment = models.CharField(
        max_length = 1024,
        default = '',
        blank = True,
        verbose_name = 'Комментарий')

    @property
    def repr(self) -> str:
        if self.id:
            return f'Заказ №{self.id}'
        else:
            return 'Заказ (новый)'

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

@receiver(pre_save, sender=TransportOrder)
def update_created(sender, instance: TransportOrder, **kwargs):
    if not instance.modified:
        instance.modified = now

@receiver(post_save, sender=TransportOrder)
def clear_cache(sender, instance: TransportOrder, **kwargs):
    cache.clear()