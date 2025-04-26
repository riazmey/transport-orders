
from django.db import models
from django.utils.timezone import now
from .enum_routepoint_action import EnumRoutepointAction


class TransportOrderRoutepoint(models.Model):

    class Meta:
        indexes = [
            models.Index(fields=['code_str'])
        ]
        ordering = ['code_str']
        verbose_name = 'Точка маршрута транспортно-логистического заказа'
        verbose_name_plural = 'Точки маршрутов транспортно-логистических заказов'

    action = models.ForeignKey(
        EnumRoutepointAction,
        on_delete = models.PROTECT,
        blank = False,
        verbose_name = 'Действие'
    )

    date = models.DateTimeField(
        default = now,
        auto_now_add = True,
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

