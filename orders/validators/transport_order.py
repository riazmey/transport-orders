
from django.core.exceptions import ValidationError
from orders.models import TransportOrder


def validate_transport_order_id(value: int):
    order_obj = TransportOrder.objects.get(id=value)
    if not order_obj:
        raise ValidationError(f'The logistics order with the identifier {value} was not found')
    return value