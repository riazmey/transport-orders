
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .transport_order import TransportOrder


class TransportOrderCargo(models.Model):
    
    class Meta:
        indexes = [
            models.Index(fields=['order']),
        ]
        ordering = ['order', 'name']
        verbose_name = 'Груз заказа'
        verbose_name_plural = 'Грузы заказов'

    order = models.ForeignKey(
        TransportOrder,
        on_delete = models.CASCADE,
        blank = False,
        verbose_name = 'Заказ'
    )

    name = models.CharField(
        max_length = 150,
        default = '',
        blank = False,
        verbose_name = 'Наименование'
    )

    weight = models.DecimalField(
        default = 0.000,
        max_digits = 15,
        decimal_places = 3,
        blank = False,
        verbose_name = 'Масса'
    )

    weight_unit = models.CharField(
        max_length = 4,
        default = '',
        blank = True,
        verbose_name = 'Единица измерения массы'
    )

    volume = models.DecimalField(
        default = 0.00,
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        verbose_name = 'Объем'
    )

    volume_unit = models.CharField(
        max_length = 4,
        default = '',
        blank = True,
        verbose_name = 'Единица измерения объема'
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
        verbose_name = 'Груз заказа'
    )

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

@receiver(pre_save, sender=TransportOrderCargo)
def update_repr(sender: TransportOrderCargo , **kwargs):
    order = TransportOrder.objects.get(id=sender.order)
    new_repr = f'{order.repr}: {sender.name}'[:255]
    if sender.repr != new_repr:
        sender.repr = new_repr
