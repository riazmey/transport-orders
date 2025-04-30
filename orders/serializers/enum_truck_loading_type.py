
from rest_framework import serializers
from orders.models import EnumTruckLoadingType


class SerializerEnumTruckLoadingType(serializers.Serializer):
    
    class Meta:

        fields = (
            'code_str',
            'repr')

        model = EnumTruckLoadingType
