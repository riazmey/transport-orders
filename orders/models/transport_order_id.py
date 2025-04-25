
from django.db.models import Field
from django.db import models
from .marketplace import Marketplace
from .transport_order import TransportOrder


class TransportOrderIDValue:

    def __init__(self, value: str | float | int):
        if isinstance(value, str):
            if ';' in value:
                parts = value.split(';')
                self.type = parts[0]
                self.value = parts[1]
            else:
                self.type = 'str'
                self.value = value
        elif isinstance(value, float):
            self.type = 'float'
            self.value = str(value)
        elif isinstance(value, int):
            self.type = 'int'
            self.value = str(value)
        else:
            raise ValueError("Unsupported type for TransportOrderIDValue")
    
    def __str__(self):
        return self.value

    def __repr__(self):
        return f'{self.value} ({self.type})'

    def value_db(self) -> str:
        return f'{self.type};{self.value}'

    def value_python(self) -> str | float | int:
        match self.type:
            case 'str':
                return self.value
            case 'float':
                return float(self.value)
            case 'int':
                return int(self.value)
            case _:
                raise ValueError(f"Unsupported type {self.type} for TransportOrderIDValue!")


class TransportOrderIDField(Field):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'VARCHAR(100)'  # Тип данных в базе данных

    def to_python(self, value):
        # Преобразуем значение из базы данных в Python-объект
        return TransportOrderIDValue(value)

    def get_prep_value(self, value):
        # Преобразуем Python-объект в значение, которое можно сохранить в базе данных
        return TransportOrderIDValue(value).value_db()


class TransportOrderID(models.Model):

    class Meta:
        unique_together = ('market', 'order', 'order_id')
        indexes = [
            models.Index(fields=['market', 'order_id']),
            models.Index(fields=['market', 'order']),
            models.Index(fields=['order_id'])
        ]
        verbose_name = 'ID транспортно-логистического заказа'
        verbose_name_plural = 'ID\'s транспортно-логистических заказов'
        ordering = ['order', 'market', 'order_code', 'object_id']

    market = models.ForeignKey(
        Marketplace,
        on_delete=models.PROTECT,
        blank=False,
        verbose_name='Площадка'
    )
    
    order = models.ForeignKey(
        TransportOrder,
        on_delete=models.PROTECT,
        blank=False,
        verbose_name='Транспортно-логистический заказ'
    )

    order_id = TransportOrderIDField(
        blank=False,
        verbose_name='Идентификатор'
    )

    order_code = models.CharField(
        blank=True,
        verbose_name='Код (человекочитаемый)'
    )

    repr = models.CharField(
        max_length=255,
        default='',
        blank=True,
        verbose_name='ID транспортно-логистического заказа'
    )
    
    def save(self, *args, **kwargs):
        self.repr = f'{self.order_id}: {self.order}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr
