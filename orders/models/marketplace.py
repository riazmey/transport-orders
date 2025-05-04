
import importlib
from django.db.models.signals import post_init
from django.dispatch import receiver
from django.db import models

from .enum_marketplace_type import EnumMarketplaceType


class Marketplace(models.Model):
    
    class Meta:
        
        constraints = [
            models.UniqueConstraint(
                fields=['type', 'url', 'login'],
                name='unique_market_type_url_login')]
        
        indexes = [models.Index(fields=['type', 'url', 'login'], name='market_type_url_login_idx')]
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'
        ordering = ['type']

    type = models.ForeignKey(
        EnumMarketplaceType,
        on_delete = models.PROTECT,
        blank = False,
        verbose_name = 'Тип площадки')

    url = models.URLField(
        default = '',
        blank = False,
        verbose_name = 'Адрес (URL)')

    login = models.CharField(
        max_length = 100,
        default = '',
        blank = False,
        verbose_name = 'Логин')

    password = models.CharField(
        max_length = 100,
        default = '',
        blank = False,
        verbose_name = 'Пароль')

    token = models.CharField(
        max_length = 256,
        default = '',
        blank = True,
        verbose_name = 'Ключ безопасности')

    @property
    def repr(self) -> str:
        if self.id:
            return f'{self.type.repr} ({self.url}; {self.login})'[:255]
        else:
            return 'Площадка (новая)'

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

@receiver(post_init, sender=Marketplace)
def initialize_ws(sender, instance: Marketplace, **kwargs):
    instance.ws = None
    if not instance.id:
        return
    try:
        name_mixin_class = f'WSMarketplace{instance.type.code_str.title()}'
        ClassMixIn = getattr(importlib.import_module('ws.marketplaces'), name_mixin_class)
        ClassBase = getattr(importlib.import_module('ws.marketplaces'), 'WSMarketplaceBase')
        MetaClass = type(name_mixin_class, (ClassMixIn, ClassBase), {})
        instance.ws = MetaClass(instance)
    except Exception as e:
        print(f"Error initializing the MixIn class: {e}")
