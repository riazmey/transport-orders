
import importlib
from django.db.models.signals import pre_save
from django.db.models.signals import post_init
from django.dispatch import receiver
from django.db import models

from .enum_marketplace_type import EnumMarketplaceType
from ws import WSMarketplaceBase


class Marketplace(models.Model):
    
    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'
        ordering = ['type']

    type = models.ForeignKey(
        EnumMarketplaceType,
        on_delete = models.PROTECT,
        db_index = True,
        blank = False,
        verbose_name = 'Тип площадки'
    )

    url = models.URLField(
        default = '',
        blank = False,
        verbose_name = 'Адрес (URL)'
    )

    login = models.CharField(
        max_length = 100,
        default = '',
        blank = False,
        verbose_name = 'Логин'
    )

    password = models.CharField(
        max_length = 100,
        default = '',
        blank = False,
        verbose_name = 'Пароль'
    )

    token = models.CharField(
        max_length = 256,
        default = '',
        blank = True,
        verbose_name = 'Ключ безопасности'
    )

    repr = models.CharField(
        max_length = 255,
        default = '',
        blank = True,
        verbose_name = 'Площадка'
    )

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

@receiver(pre_save, sender=Marketplace)
def update_repr(sender, instance: Marketplace, **kwargs):
    new_repr = ''
    if instance:
        new_repr = f'{instance.type.repr} ({instance.url}; {instance.login})'[:255]
    if instance.repr != new_repr:
        instance.repr = new_repr

@receiver(post_init, sender=Marketplace)
def initialize_ws(sender, instance: Marketplace, **kwargs):
    instance.ws = None
    if not instance.id:
        return
    try:
        name_mixin_class = f'WSMarketplace{instance.type.code_str.title()}'
        ClassMixIn = getattr(importlib.import_module('ws'), name_mixin_class)
        MetaClass = type(name_mixin_class, (ClassMixIn, WSMarketplaceBase), {})
        instance.ws = MetaClass(instance)
    except Exception as e:
        print(f"Error initializing the MixIn class: {e}")
