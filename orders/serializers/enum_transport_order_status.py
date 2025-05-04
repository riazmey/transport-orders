
from rest_framework import serializers
from orders.models import EnumTransportOrderStatus


class SerializerEnumTransportOrderStatus(serializers.ModelSerializer):

    class Meta:

        fields = (
            'code_str',
            'repr')

        model = EnumTransportOrderStatus
