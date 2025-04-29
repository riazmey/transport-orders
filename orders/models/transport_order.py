
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now

from .marketplace import Marketplace
from .counterparty import Counterparty
from .enum_transport_order_status import EnumTransportOrderStatus


class TransportOrder(models.Model):
    
    class Meta:
        indexes = [
            models.Index(fields=['market']),
            models.Index(fields=['created']),
            models.Index(fields=['status']),
        ]
        ordering = ['market', 'created', 'status']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    market = models.ForeignKey(
        Marketplace,
        on_delete = models.PROTECT,
        blank = False,
        verbose_name = 'Торговая площадка'
    )

    created = models.DateTimeField(
        blank = False,
        verbose_name = 'Дата создания'
    )

    status = models.ForeignKey(
        EnumTransportOrderStatus,
        on_delete = models.PROTECT,
        blank = False,
        verbose_name = 'Статус'
    )

    counterparty = models.ForeignKey(
        Counterparty,
        on_delete = models.PROTECT,
        blank = False,
        verbose_name = 'Контрагент (заказчик)'
    )

    currency = models.CharField(
        max_length = 3,
        default = '',
        blank = False,
        verbose_name = 'Валюта'
    )
 
    price = models.DecimalField(
        default = 0.00,
        max_digits = 15,
        decimal_places = 2,
        blank = False,
        verbose_name = 'Цена'
    )

    rate_vat = models.CharField(
        max_length = 3,
        default = '',
        blank = False,
        verbose_name = 'Ставка НДС'
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

@receiver(pre_save, sender=TransportOrder)
def update_repr(sender: TransportOrder, **kwargs):
    new_repr = f'Заказ №{sender.id}'[:255]
    if sender.repr != new_repr:
        sender.repr = new_repr

@receiver(pre_save, sender=TransportOrder)
def update_created(sender: TransportOrder, **kwargs):
    if not sender.created:
        sender.created = now
