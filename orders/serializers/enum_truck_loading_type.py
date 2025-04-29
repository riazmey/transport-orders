
from rest_framework import serializers
from orders.models import EnumTruckLoadingType


class SerializerEnumTruckLoadingType(serializers.Serializer):
    
    class Meta:
        model = EnumTruckLoadingType
        fields = (
            'code_str',
            'repr'
        )
