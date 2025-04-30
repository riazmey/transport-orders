
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Counterparty(models.Model):
    
    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['inn', 'kpp'],
                name='unique_inn_per_kpp')]

        indexes = [models.Index(fields=['inn', 'kpp'])]
        ordering = ["name"]
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"

    name = models.CharField(
        max_length=255,
        default="",
        blank=False,
        verbose_name="Наименование (для поиска)")

    name_full = models.CharField(
        max_length=255,
        default="",
        blank=False,
        verbose_name="Наименование (полное)")

    inn = models.CharField(
        max_length=12,
        default="",
        blank=False,
        verbose_name="ИНН")

    kpp = models.CharField(
        max_length=9,
        default="",
        blank=True,
        verbose_name="КПП")
    
    repr = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name="Контрагент")

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

    def __eq__(self, value):
        if isinstance(value, str):
            return self.name == value
        return super().__eq__(value)

@receiver(pre_save, sender=Counterparty)
def update_repr(sender, instance: Counterparty , **kwargs):
    new_repr = f'{instance.name} ({instance.inn}/{instance.kpp})'[:255]
    if instance.repr != new_repr:
        instance.repr = new_repr
