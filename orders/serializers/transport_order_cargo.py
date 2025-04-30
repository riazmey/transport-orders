
from rest_framework import serializers
from orders.models import TransportOrderCargo


class SerializerTransportOrderCargo(serializers.Serializer):

    class Meta:

        fields = (
            'order',
            'name',
            'weight',
            'weight_unit',
            'volume',
            'volume_unit',
            'comment',
            'repr')

        model = TransportOrderCargo
