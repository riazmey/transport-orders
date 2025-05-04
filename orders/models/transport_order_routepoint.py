
from django.db import models

from .enum_routepoint_action import EnumRoutepointAction
from .transport_order import TransportOrder


class TransportOrderRoutepoint(models.Model):

    class Meta:

        indexes = [
            models.Index(fields=['order'], name='route_order_idx'),
            models.Index(fields=['order', 'address'], name='route_order_addr_idx')]

        ordering = ['order', 'date_start']
        verbose_name = 'Точка маршрута заказа'
        verbose_name_plural = 'Точки маршрутов заказов'

    order = models.ForeignKey(
        TransportOrder,
        on_delete = models.CASCADE,
        related_name = 'order_relate_routepoint',
        blank = False,
        verbose_name = 'Заказ')

    action = models.ForeignKey(
        EnumRoutepointAction,
        on_delete = models.PROTECT,
        blank = False,
        verbose_name = 'Действие')

    date_start = models.DateTimeField(
        blank = True,
        null = True,
        verbose_name = 'Дата начала действия')

    date_end = models.DateTimeField(
        blank = True,
        null = True,
        verbose_name = 'Дата окончания действия')

    address = models.CharField(
        max_length = 1024,
        default = '',
        blank = False,
        verbose_name = 'Адрес')

    counterparty = models.CharField(
        max_length = 255,
        default = '',
        blank = True,
        verbose_name = 'Контрагент')

    contact_person = models.CharField(
        max_length = 255,
        default = '',
        blank = True,
        verbose_name = 'Контактное лицо')

    comment = models.CharField(
        max_length = 1024,
        default = '',
        blank = True,
        verbose_name = 'Комментарий')

    @property
    def repr(self) -> str:
        if self.order:
            return f'Точка маршрута {self.order.repr}: {self.address}'[:255]
        else:
            return 'Точка маршрута (новая)'

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr
