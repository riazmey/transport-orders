
from rest_framework import serializers
from orders.models import EnumTransportOrderStatus


class SerializerEnumTransportOrderStatus(serializers.Serializer):
    
    class Meta:

        fields = (
            'code_str',
            'repr')

        model = EnumTransportOrderStatus
