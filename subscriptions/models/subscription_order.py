
from django.db import models

from orders.models import TransportOrder
from .subscription import Subscription


class SubscriptionOrder(models.Model):
    
    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['subscription', 'order'],
                name='unique_subscription_order')]

        indexes = [
            models.Index(fields=['subscription'], name='subscription_order_idx')]

        ordering = ['subscription']
        verbose_name = 'Заказ подписки'
        verbose_name_plural = 'Заказы подписок'

    subscription = models.ForeignKey(
        Subscription,
        on_delete = models.CASCADE,
        blank = False,
        verbose_name = 'Пользователь')
    
    order = models.OneToOneField(
        TransportOrder,
        on_delete = models.CASCADE,
        blank = False,
        verbose_name = 'Заказ')

    @property
    def repr(self) -> str:
        if self.id:
            return f'{self.subscription} - {self.order})'[:255]
        else:
            return 'Заказ подписки (новый)'

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr
