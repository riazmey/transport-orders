
from django.db.models.signals import post_init
from django.dispatch import receiver
from django.db import transaction
from django.db import models
from .enum_marketplace_type import EnumMarketplaceType


class Marketplace(models.Model):
    
    type = models.ForeignKey(
        EnumMarketplaceType,
        on_delete=models.PROTECT,
        db_index=True,
        blank=False,
        verbose_name='Тип площадки'
    )

    url = models.URLField(
        max_length=255,
        default='',
        blank=False,
        verbose_name='Адрес (URL)'
    )

    login = models.CharField(
        max_length=100,
        default='',
        blank=False,
        verbose_name='Логин'
    )

    password = models.CharField(
        max_length=128,
        default='',
        blank=False,
        verbose_name='Пароль'
    )

    repr = models.CharField(
        max_length=255,
        default='',
        blank=True,
        verbose_name='Площадка'
    )

    def save(self, *args, **kwargs):
        self.repr = f'{self.type} ({self.organization})'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'
        ordering = ['type', 'organization']


@receiver(post_init, sender=Marketplace)
def initialize_api(sender, instance, **kwargs):
    if instance.id:
        try:
            ClassMixIn = globals().get(instance.type.name)
            if ClassMixIn is None:
                raise ValueError(f"Класс для типа {instance.type.name} не найден")
            MetaClass = type(f'API{instance.type.name}', (ClassMixIn, BaseAPI), {})
            instance.api = MetaClass(instance)
        except Exception as e:
            print(f"Ошибка при инициализации API: {e}")
            instance.api = None
    else:
        instance.api = None


class BaseAPI:

    def __init__(self, market: Marketplace):
        self.market = market
        self.url = market.url
        self.login = market.login
        self.password = market.password

    @transaction.atomic
    def order_import(self, **kwargs) -> (list[dict], bool):
        result = []
        data, success = self.order_get(**kwargs)
        if success:
            for order_data in data:
                result += self._order_import(**order_data)
        return result, success

    def _order_import(self, **kwargs) -> list[dict]:
        result = []
        return result
