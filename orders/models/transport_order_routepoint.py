
from datetime import datetime
from django.db import models
from django.utils.timezone import now
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .enum_routepoint_action import EnumRoutepointAction
from .transport_order import TransportOrder


class TransportOrderRoutepoint(models.Model):

    class Meta:
        indexes = [models.Index(fields=['order'])]
        ordering = ['order', 'date']
        verbose_name = 'Точка маршрута заказа'
        verbose_name_plural = 'Точки маршрутов заказов'

    order = models.ForeignKey(
        TransportOrder,
        on_delete = models.CASCADE,
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

    repr = models.CharField(
        max_length = 255,
        default = '',
        blank = True,
        verbose_name = 'Точка маршрута заказа')

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

@receiver(pre_save, sender=TransportOrderRoutepoint)
def update_repr(sender, instance: TransportOrderRoutepoint , **kwargs):
    order = TransportOrder.objects.get(id=instance.order)
    new_repr = f'Точка маршрута {order.repr}: {instance.address}'[:255]
    if instance.repr != new_repr:
        instance.repr = new_repr

@receiver(pre_save, sender=TransportOrderRoutepoint)
def update_date(sender, instance: TransportOrderRoutepoint, **kwargs):
    this_day = datetime.today().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=None)
    if not instance.date_start or not instance.date_end:
        instance.date_start = this_day + datetime.timedelta(days=1)
        instance.date_end = instance.date_start + datetime.timedelta(
            hours=23,
            minutes=59,
            seconds=59,
            microsecond=999999)