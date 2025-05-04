
from rest_framework import serializers
from orders.models import EnumTruckLoadingType


class SerializerEnumTruckLoadingType(serializers.ModelSerializer):
    
    class Meta:

        fields = (
            'code_str',
            'repr')

        model = EnumTruckLoadingType
