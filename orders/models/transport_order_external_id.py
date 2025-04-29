
from django.db import models
from django.db.models import CharField
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .marketplace import Marketplace
from .transport_order import TransportOrder


class TransportOrderExternalIDValue:
    """Represents and validates transport order external ID values.
    
    Supports serialization/deserialization of different data types
    into a unified string format for database storage.
    
    Format: <type>;<value>
    Supported types: str, float, int
    """

    def __init__(self, value: str | float | int):
        if isinstance(value, str):
            if ';' in value:
                if value.count(';') != 1:
                    raise ValueError("Invalid format for string value. Expected exactly one ';'")
                parts = value.split(';')
                if parts[0] not in {'str', 'float', 'int'}:
                    raise ValueError(f"Invalid type specifier: {parts[0]}")
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
            raise ValueError("Unsupported type for TransportOrderExternalIDValue")
    
    def __str__(self):
        return self.value

    def __repr__(self):
        return f'{self.value} ({self.type})'

    def __eq__(self, other):
        if isinstance(other, TransportOrderExternalIDValue):
            return self.type == other.type and self.value == other.value
        return False

    def __hash__(self):
        return hash((self.type, self.value))

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
                raise ValueError(f"Unsupported type {self.type} for TransportOrderExternalIDValue!")


class TransportOrderExternalIDField(CharField):

    def __init__(self, max_length=100, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_length = max_length

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['max_length'] = self.max_length
        return name, path, args, kwargs

    def db_type(self, connection):
        return f'VARCHAR({self.max_length})'

    def to_python(self, value):
        return TransportOrderExternalIDValue(value)

    def get_prep_value(self, value):
        return TransportOrderExternalIDValue(value).value_db()


class TransportOrderExternalID(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['market', 'order', 'external_id'],
                name='unique_order_per_market'
            )
        ]
        indexes = [
            models.Index(fields=['market', 'external_id'], name='market_order_id_idx'),
            models.Index(fields=['order_id'], name='order_id_idx')
        ]
        ordering = ['order', 'market', 'external_code', 'external_id']
        verbose_name = 'Идентификатор заказа'
        verbose_name_plural = 'Идентификаторы заказов'

    market = models.ForeignKey(
        Marketplace,
        on_delete = models.PROTECT,
        blank = False,
        verbose_name = 'Площадка'
    )
    
    order = models.ForeignKey(
        TransportOrder,
        on_delete = models.CASCADE,
        blank = False,
        verbose_name = 'Заказ'
    )

    external_id = TransportOrderExternalIDField(
        max_length = 40,
        blank = False,
        verbose_name = 'Идентификатор'
    )

    external_code = models.CharField(
        max_length = 50,
        default = '',
        blank = True,
        verbose_name = 'Код (человекочитаемый)'
    )

    repr = models.CharField(
        max_length = 255,
        default = '',
        blank = True,
        verbose_name = 'Идентификатор заказа'
    )

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

@receiver(pre_save, sender=TransportOrderExternalID)
def update_repr(sender: TransportOrderExternalID , **kwargs):
    order = TransportOrder.objects.get(id=sender.order)
    marketplace = Marketplace.objects.get(id=sender.market)
    new_repr = f'ID {order.repr}, {marketplace.repr}: {sender.external_id}'[:255]
    if sender.repr != new_repr:
        sender.repr = new_repr
