
from django.core.exceptions import ValidationError


def validate_transport_order_truck_reqts_temperature(value: int):
    min_value = -273
    max_value = 35
    if value > 35:
        raise ValidationError(f'The temperature must not be set above {max_value} ℃')
    if value < min_value:
        raise ValidationError(f'The temperature must not be set below {min_value} ℃')
    return value
