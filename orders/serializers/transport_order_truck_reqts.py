
from rest_framework import serializers
from orders.models import TransportOrderTruckReqts
from .transport_order_truck_reqts_loading_type import SerializerTransportOrderTruckReqtsLoadingType


class SerializerTransportOrderTruckReqts(serializers.Serializer):

    loading_types = SerializerTransportOrderTruckReqtsLoadingType()

    class Meta:

        fields = (
            'order',
            'weight',
            'weight_unit',
            'volume',
            'volume_unit',
            'refrigeration',
            'temperature',
            'loading_types'
            'comment',
            'repr')
        
        model = TransportOrderTruckReqts
