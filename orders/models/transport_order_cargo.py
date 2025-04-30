
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .transport_order import TransportOrder


class TransportOrderCargo(models.Model):
    
    class Meta:
        indexes = [models.Index(fields=['order'])]
        ordering = ['order', 'name']
        verbose_name = 'Груз заказа'
        verbose_name_plural = 'Грузы заказов'

    order = models.ForeignKey(
        TransportOrder,
        on_delete = models.CASCADE,
        blank = False,
        verbose_name = 'Заказ')

    name = models.CharField(
        max_length = 150,
        default = '',
        blank = False,
        verbose_name = 'Наименование')

    hazard_class = models.CharField(
        max_length = 5,
        default = '',
        blank = False,
        verbose_name = 'Класс опасности')

    weight = models.DecimalField(
        default = 0.000,
        max_digits = 15,
        decimal_places = 3,
        blank = False,
        verbose_name = 'Масса')

    weight_unit = models.CharField(
        max_length = 4,
        default = '',
        blank = True,
        verbose_name = 'Единица измерения массы')

    volume = models.DecimalField(
        default = 0.00,
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        verbose_name = 'Объем')

    volume_unit = models.CharField(
        max_length = 4,
        default = '',
        blank = True,
        verbose_name = 'Единица измерения объема')

    comment = models.CharField(
        max_length = 1024,
        default = '',
        blank = True,
        verbose_name = 'Комментарий')

    repr = models.CharField(
        max_length = 255,
        default = '',
        blank = True,
        verbose_name = 'Груз заказа')

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

@receiver(pre_save, sender=TransportOrderCargo)
def update_repr(sender, instance: TransportOrderCargo , **kwargs):
    order = TransportOrder.objects.get(id=instance.order)
    new_repr = f'{order.repr}: {instance.name}'[:255]
    if instance.repr != new_repr:
        instance.repr = new_repr

@receiver(pre_save, sender=TransportOrderCargo)
def update_hazard_class(sender, instance: TransportOrderCargo , **kwargs):
    if not instance.hazard_class:
        instance.hazard_class = '0'
