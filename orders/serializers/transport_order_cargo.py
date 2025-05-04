
from rest_framework import serializers
from orders.models import TransportOrderCargo


class SerializerTransportOrderCargo(serializers.ModelSerializer):

    class Meta:

        fields = (
            'name',
            'hazard_class',
            'weight',
            'weight_unit',
            'volume',
            'volume_unit',
            'comment',
            'repr')

        model = TransportOrderCargo
