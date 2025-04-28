
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .enum_routepoint_action import EnumRoutepointAction
from .transport_order import TransportOrder


class TransportOrderRoutepoint(models.Model):

    class Meta:
        indexes = [
            models.Index(fields=['order'])
        ]
        ordering = ['order', 'date']
        verbose_name = 'Точка маршрута заказа'
        verbose_name_plural = 'Точки маршрутов заказов'

    order = models.ForeignKey(
        TransportOrder,
        on_delete = models.CASCADE,
        blank = False,
        verbose_name = 'Заказ'
    )

    action = models.ForeignKey(
        EnumRoutepointAction,
        on_delete = models.PROTECT,
        blank = False,
        verbose_name = 'Действие'
    )

    date = models.DateTimeField(
        #auto_now_add = True,
        blank = False,
        verbose_name = 'Дата'
    )

    address = models.CharField(
        max_length = 1024,
        default = '',
        blank = False,
        verbose_name = 'Адрес'
    )

    counterparty = models.CharField(
        max_length = 255,
        default = '',
        blank = True,
        verbose_name = 'Контрагент'
    )

    contact_person = models.CharField(
        max_length = 255,
        default = '',
        blank = True,
        verbose_name = 'Контактное лицо'
    )

    comment = models.CharField(
        max_length = 1024,
        default = '',
        blank = True,
        verbose_name = 'Комментарий'
    )

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

@receiver(pre_save, sender=TransportOrderRoutepoint)
def update_repr(sender: TransportOrderRoutepoint , **kwargs):
    order = TransportOrder.objects.get(id=sender.order)
    new_repr = f'Точка маршрута {order.repr}: {sender.address}'
    if sender.repr != new_repr:
        sender.repr = new_repr

