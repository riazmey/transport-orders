
from datetime import datetime
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .enum_routepoint_action import EnumRoutepointAction
from .transport_order import TransportOrder


class TransportOrderRoutepoint(models.Model):

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['order', 'address', 'date_start'],
                name='unique_route_order_addr_date')]

        indexes = [
            models.Index(fields=['order'], name='route_order_idx'),
            models.Index(fields=['order', 'address'], name='route_order_addr_idx'),
            models.Index(fields=['order', 'address', 'date_start'], name='route_order_addr_date_idx')]
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
        blank = False,
        verbose_name = 'Дата начала действия')

    date_end = models.DateTimeField(
        blank = False,
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

@receiver(pre_save, sender=TransportOrderRoutepoint)
def update_date(sender, instance: TransportOrderRoutepoint, **kwargs):

    if not instance.date_start:
        this_day = datetime.today().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=None)
        instance.date_start = this_day + datetime.timedelta(days=1)

    if not instance.date_end:
        instance.date_end = instance.date_start + datetime.timedelta(
            hours=23,
            minutes=59,
            seconds=59,
            microsecond=999999)
