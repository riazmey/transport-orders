
from rest_framework import serializers
from orders.models import TransportOrderTruckReqtsLoadingType
from .enum_truck_loading_type import SerializerEnumTruckLoadingType


class SerializerTransportOrderTruckReqtsLoadingType(serializers.Serializer):

    loading_type = SerializerEnumTruckLoadingType()

    class Meta:

        fields = (
            'order_truck_reqts',
            'loading_type',
            'repr')

        model = TransportOrderTruckReqtsLoadingType