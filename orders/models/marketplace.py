
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
        max_length = 128,
        default = '',
        blank = False,
        verbose_name = 'Пароль'
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
def update_repr(sender: Marketplace , **kwargs):
    marketplace_type = EnumMarketplaceType.objects.get(id=sender.type)
    new_repr = f'{marketplace_type.repr} ({sender.url})'
    if sender.repr != new_repr:
        sender.repr = new_repr

@receiver(post_init, sender=Marketplace)
def initialize_api(sender: Marketplace, **kwargs):
    try:
        marketplace_type = EnumMarketplaceType.objects.get(id=sender.type)
        name_mixin_class = f'WSMarketplace{marketplace_type.name.title()}'
        ClassMixIn = getattr(importlib.import_module(f'ws.{name_mixin_class}'), name_mixin_class)
        #ClassMixIn = globals().get(name_mixin_class)
        if ClassMixIn is None:
            raise ValueError(f'A MixIn class with name \'{name_mixin_class}\' for the type marketplace \'{marketplace_type.name}\' not found')
        MetaClass = type(name_mixin_class, (ClassMixIn, WSMarketplaceBase), {})
        sender.api = MetaClass(sender)
    except Exception as e:
        print(f"Error initializing the MixIn class: {e}")
        sender.api = None
