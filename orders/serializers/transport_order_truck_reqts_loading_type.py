
from rest_framework import serializers
from orders.models import TransportOrderTruckReqtsLoadingType
from .enum_truck_loading_type import SerializerEnumTruckLoadingType


class SerializerTransportOrderTruckReqtsLoadingType(serializers.ModelSerializer):

    loading_type = SerializerEnumTruckLoadingType()

    class Meta:

        fields = (
            'loading_type',
            'repr')

        model = TransportOrderTruckReqtsLoadingType