
from django.db import models

class EnumMarketplaceType(models.Model):

    class Meta:
        indexes = [
            models.Index(fields=['code_str'])
        ]
        ordering = ['name']
        verbose_name = 'API площадки'
        verbose_name_plural = 'API площадок'

    code_str = models.CharField(
        max_length=50,
        default='',
        blank=False,
        unique=True,
        verbose_name='Код (строковый)'
    )

    repr = models.CharField(
        max_length=255,
        default='',
        blank=False,
        verbose_name='API площадки'
    )

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr
