
from django.db.models import Field
from django.db import models
from .marketplace import Marketplace
from .transport_order import TransportOrder


class TransportOrderIDValue:
    """Represents and validates transport order ID values.
    
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
            raise ValueError("Unsupported type for TransportOrderIDValue")
    
    def __str__(self):
        return self.value

    def __repr__(self):
        return f'{self.value} ({self.type})'

    def __eq__(self, other):
        if isinstance(other, TransportOrderIDValue):
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
                raise ValueError(f"Unsupported type {self.type} for TransportOrderIDValue!")


class TransportOrderIDField(Field):

    def __init__(self, *args, max_length=100, **kwargs):
        self.max_length = max_length
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['max_length'] = self.max_length
        return name, path, args, kwargs

    def db_type(self, connection):
        return f'VARCHAR({self.max_length})'

    def to_python(self, value):
        return TransportOrderIDValue(value)

    def get_prep_value(self, value):
        return TransportOrderIDValue(value).value_db()


class TransportOrderID(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['market', 'order', 'order_id'],
                name='unique_order_per_market'
            )
        ]
        indexes = [
            models.Index(fields=['market', 'order_id'], name='market_order_id_idx'),
            models.Index(fields=['order_id'], name='order_id_idx')
        ]
        verbose_name = 'ID транспортно-логистического заказа'
        verbose_name_plural = 'ID\'s транспортно-логистических заказов'
        ordering = ['order', 'market', 'order_code', 'object_id']

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
        verbose_name = 'Транспортно-логистический заказ'
    )

    order_id = TransportOrderIDField(
        blank = False,
        verbose_name = 'Идентификатор'
    )

    order_code = models.CharField(
        default = '',
        blank = True,
        verbose_name = 'Код (человекочитаемый)'
    )

    repr = models.CharField(
        max_length = 255,
        default = '',
        blank = True,
        verbose_name = 'ID транспортно-логистического заказа'
    )

    @property
    def repr(self):
        return f'{self.order_id}: {self.order}'

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr
