
from django.core.exceptions import ValidationError
from orders.models import Marketplace


def validate_marketplace_id(value: int):
    if not Marketplace.objects.filter(id=value).exists():
        raise ValidationError(f'The marketplace with the identifier {value} was not found')
    return value
