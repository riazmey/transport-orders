
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

from .transport_order import TransportOrder


class TransportOrderCargo(models.Model):
    
    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['order', 'name'],
                name='unique_cargo_order_name')]
        
        indexes = [models.Index(fields=['order', 'name'], name='cargo_order_name_idx')]
        ordering = ['order', 'name']
        verbose_name = 'Груз заказа'
        verbose_name_plural = 'Грузы заказов'

    order = models.ForeignKey(
        TransportOrder,
        on_delete = models.CASCADE,
        related_name = 'order_relate_cargo',
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

    weight = models.FloatField(
        default = 0.000,
        blank = False,
        verbose_name = 'Масса')

    weight_unit = models.CharField(
        max_length = 4,
        default = '',
        blank = True,
        verbose_name = 'Единица измерения массы')

    volume = models.FloatField(
        default = 0.00,
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
    
    @property
    def repr(self) -> str:
        if self.order:
            return f'{self.order.repr}: {self.name}'[:255]
        else:
            return 'Груз заказа (новый)'

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

@receiver(post_save, sender=TransportOrderCargo)
def clear_cache(sender, instance: TransportOrderCargo, **kwargs):
    cache.clear()