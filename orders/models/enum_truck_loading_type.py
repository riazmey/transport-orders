
from django.db import models

class EnumTruckLoadingType(models.Model):

    class Meta:
        indexes = [models.Index(fields=['code_str'])]
        ordering = ['code_str']
        verbose_name = 'Тип загрузки грузовика'
        verbose_name_plural = 'Типы загрузок грузовиков'

    code_str = models.CharField(
        max_length = 50,
        default = '',
        blank = False,
        unique = True,
        verbose_name = 'Код (строковый)')

    repr = models.CharField(
        max_length = 255,
        default = '',
        blank = False,
        verbose_name = 'Тип загрузки грузовика')

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr
