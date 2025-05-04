
from django.core.exceptions import ValidationError
from orders.models import Marketplace
from orders.models import TransportOrder


def validate_transport_order_id(value: int):
    if not TransportOrder.objects.filter(id=value).exists():
        raise ValidationError(f'The transport order with the identifier {value} was not found')
    return value

def validate_transport_order_market(value: int):
    if not Marketplace.objects.filter(id=value).exists():
        raise ValidationError(f'The marketplace with the identifier {value} was not found')
    return value